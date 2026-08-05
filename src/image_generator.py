import os
import json
import time
from io import BytesIO
from PIL import Image, ImageFilter
from google import genai
from google.genai import types
from config.settings import IMAGES_DIR

def generate_images(story_path):
    print("🎨 Generating Images using Google Gemini (With Free Tier Safety Limits)...")
    
    with open(story_path, 'r', encoding='utf-8') as f:
        story_data = json.load(f)

    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("❌ CRITICAL ERROR: GEMINI_API_KEY not found!")
        return False

    client = genai.Client(api_key=api_key)
    images_success = True

    # গুগলের লেটেস্ট লাইটওয়েট এবং ফাস্ট ইমেজ মডেল
    image_models_to_try = ['gemini-3.1-flash-lite-image', 'gemini-3.1-flash-image']

    for scene in story_data['scenes']:
        scene_num = scene['scene_number']
        img_path = os.path.join(IMAGES_DIR, f"scene_{scene_num}.jpg")

        # আগের ছবিগুলো স্কিপ করবে (যাতে খামোখা API লিমিট নষ্ট না হয়)
        if os.path.exists(img_path):
            print(f"⏭️ Scene {scene_num} already exists. Skipping...")
            continue

        raw_prompt = scene.get('image_prompt', "A cute cartoon character")
        enhanced_prompt = f"3D Pixar style, masterpiece, highly detailed, vibrant colors, {raw_prompt}, wide angle shot, full body"
        
        image_downloaded = False
        
        for attempt in range(3):
            for model_name in image_models_to_try:
                try:
                    print(f"🔄 Trying model: {model_name} for Scene {scene_num}...")
                    
                    response = client.models.generate_images(
                        model=model_name,
                        prompt=enhanced_prompt,
                        config=types.GenerateImagesConfig(
                            number_of_images=1,
                            output_mime_type="image/jpeg",
                            aspect_ratio="1:1"
                        )
                    )
                    
                    if response.generated_images:
                        image_bytes = response.generated_images[0].image.image_bytes
                        original_img = Image.open(BytesIO(image_bytes)).convert("RGB")
                        
                        target_width, target_height = 1080, 1920
                        
                        fg_img = original_img.resize((1080, 1080))
                        bg_img = original_img.resize((target_width, target_height))
                        bg_img = bg_img.filter(ImageFilter.GaussianBlur(radius=35))
                        
                        y_offset = (target_height - 1080) // 2
                        bg_img.paste(fg_img, (0, y_offset))
                        
                        bg_img.save(img_path, "JPEG", quality=95)
                        
                        print(f"✅ Scene {scene_num} image saved successfully!")
                        image_downloaded = True
                        
                        # 🌟 আসল ম্যাজিক: রেট লিমিট থেকে বাঁচতে ২০ সেকেন্ডের ব্রেক!
                        print("⏳ Respecting Free Tier Limits: Waiting 20 seconds before next request...")
                        time.sleep(20) 
                        break 
                    else:
                        print("⚠️ No image returned. Switching model...")
                        
                except Exception as e:
                    print(f"⚠️ Request failed: {e}. Switching model...")
                    time.sleep(5)
                    
            if image_downloaded:
                break
            else:
                print("⏳ Quota limit reached or models busy. Waiting 60 seconds before retry...")
                time.sleep(60) # কোনো কারণে এরর দিলে ১ মিনিট ব্রেক নেবে

        if not image_downloaded:
            print(f"❌ CRITICAL ERROR: Failed to generate image for Scene {scene_num}")
            images_success = False
            break

    return images_success
