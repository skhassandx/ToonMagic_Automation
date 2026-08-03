import os
import json
import base64
import time  # 🌟 সার্ভারকে বিশ্রাম দেওয়ার জন্য time মডিউল যুক্ত করা হলো
from google import genai
from config.settings import IMAGES_DIR

def generate_images(story_path):
    with open(story_path, 'r', encoding='utf-8') as f:
        story_data = json.load(f)

    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("❌ CRITICAL ERROR: GEMINI_API_KEY not found!")
        return False

    client = genai.Client(api_key=api_key)
    images_success = True

    for scene in story_data['scenes']:
        scene_num = scene['scene_number']
        img_path = os.path.join(IMAGES_DIR, f"scene_{scene_num}.jpg")

        if os.path.exists(img_path):
            continue

        prompt = scene.get('image_prompt', "3D Pixar style cartoon")
        enhanced_prompt = f"3D Pixar animation style, {prompt}, masterpiece, highly detailed, vibrant colors"
        print(f"🎨 Generating Image for Scene {scene_num} using Gemini API...")

        # 🌟 গুগলের 429 Error এড়ানোর জন্য রিট্রাই লুপ
        max_retries = 3
        for attempt in range(max_retries):
            try:
                interaction = client.interactions.create(
                    model="gemini-3.1-flash-image",
                    input=enhanced_prompt
                )
                
                if interaction and interaction.output_text:
                    with open(img_path, "wb") as img_file:
                        img_file.write(base64.b64decode(interaction.output_text))
                    print(f"✅ Scene {scene_num} generated with Gemini!")
                    
                    # 🌟 সফল হলে পরের ছবির আগে ৩০ সেকেন্ড বিশ্রাম নেবে
                    if scene_num < len(story_data['scenes']):
                        print("⏳ Waiting 30 seconds before next image to respect API Rate Limit...")
                        time.sleep(30)
                    break  # সফল হলে রিট্রাই লুপ থেকে বের হয়ে যাবে
                else:
                    print(f"❌ Failed to receive image data for Scene {scene_num}")
                    images_success = False
                    break
                    
            except Exception as e:
                error_msg = str(e)
                print(f"⚠️ API Error on attempt {attempt + 1}: {error_msg}")
                
                # 🌟 যদি কোটা বা রেট লিমিট (429) এরর আসে, তবে ৬০ সেকেন্ড অপেক্ষা করে আবার চেষ্টা করবে
                if "429" in error_msg or "quota" in error_msg.lower() or "too_many_requests" in error_msg.lower():
                    if attempt < max_retries - 1:
                        print("⏳ Rate limit hit! Waiting 60 seconds before retrying...")
                        time.sleep(60)
                    else:
                        print("❌ Maximum retries reached. Gemini API Quota exceeded.")
                        images_success = False
                else:
                    print(f"❌ Gemini Image Error: {e}")
                    images_success = False
                    break

        if not images_success:
            break

    return images_success
