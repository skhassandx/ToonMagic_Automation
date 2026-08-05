import os
import json
import time
from io import BytesIO
from PIL import Image, ImageFilter
from huggingface_hub import InferenceClient
from config.settings import IMAGES_DIR

def generate_images(story_path):
    print("🎨 Generating Images using Hugging Face (Free & Stable Model)...")
    
    with open(story_path, 'r', encoding='utf-8') as f:
        story_data = json.load(f)

    api_key = os.environ.get("HF_API_KEY")
    if not api_key:
        print("❌ CRITICAL ERROR: HF_API_KEY not found in environment variables!")
        return False

    client = InferenceClient(token=api_key)
    images_success = True

    for scene in story_data['scenes']:
        scene_num = scene['scene_number']
        img_path = os.path.join(IMAGES_DIR, f"scene_{scene_num}.jpg")

        if os.path.exists(img_path):
            continue

        prompt = scene.get('image_prompt', "A cute cartoon character")
        # 🌟 প্রফেশনাল প্রম্পট
        enhanced_prompt = f"3D Pixar style, masterpiece, highly detailed, vibrant colors, {prompt}, wide angle shot, full body"
        
        image_downloaded = False
        
        for attempt in range(3):
            try:
                print(f"🔄 Trying to generate image for Scene {scene_num} (Attempt {attempt+1})...")
                
                # 🌟 ১০০% ফ্রি এবং স্ট্যাবল মডেল ব্যবহার করা হচ্ছে (কোনো 402 Error আসবে না)
                image = client.text_to_image(
                    enhanced_prompt,
                    model="stabilityai/stable-diffusion-2-1"
                )
                
                # 🌟 সিনেমাটিক ব্লার প্যাডিং
                original_img = image.convert("RGB")
                target_width, target_height = 1080, 1920
                
                # আসল ছবি স্কয়ার (৭৬৮x৭৬৮) করে ব্যাকগ্রাউন্ড ব্লার করা
                fg_img = original_img.resize((1080, 1080))
                bg_img = original_img.resize((target_width, target_height))
                bg_img = bg_img.filter(ImageFilter.GaussianBlur(radius=35))
                
                y_offset = (target_height - 1080) // 2
                bg_img.paste(fg_img, (0, y_offset))
                
                bg_img.save(img_path, "JPEG", quality=95)
                
                print(f"✅ Scene {scene_num} image saved successfully!")
                image_downloaded = True
                break
                
            except Exception as e:
                print(f"⚠️ Image generation failed: {e}")
                print("⏳ Waiting 10 seconds before retrying...")
                time.sleep(10)

        if not image_downloaded:
            print(f"❌ CRITICAL ERROR: Failed to generate image for Scene {scene_num}")
            images_success = False
            break

    return images_success
