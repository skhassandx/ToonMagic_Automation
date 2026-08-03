import os
import json
import base64
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

        try:
            # 🌟 আপনার স্ক্রিনশট অনুযায়ী gemini-3.1-flash-image মডেল ব্যবহার
            interaction = client.interactions.create(
                model="gemini-3.1-flash-image",
                input=enhanced_prompt
            )
            
            # Base64 এনকোডেড ডেটা রিসিভ করে ছবিতে সেভ করা
            if interaction and interaction.output_text:
                with open(img_path, "wb") as img_file:
                    img_file.write(base64.b64decode(interaction.output_text))
                print(f"✅ Scene {scene_num} generated with Gemini!")
            else:
                 print(f"❌ Failed to receive image data for Scene {scene_num}")
                 images_success = False
                 break
                 
        except Exception as e:
            print(f"❌ Gemini Image Error: {e}")
            images_success = False
            break

    return images_success
