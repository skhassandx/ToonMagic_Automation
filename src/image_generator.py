import os
import json
import time
import random
import urllib.parse
import requests
from io import BytesIO
from PIL import Image, ImageFilter
from config.settings import IMAGES_DIR

def generate_images(story_path):
    print("🎨 Generating Images using Unlimited Free API (No Keys Required)...")
    
    with open(story_path, 'r', encoding='utf-8') as f:
        story_data = json.load(f)

    images_success = True

    for scene in story_data['scenes']:
        scene_num = scene['scene_number']
        img_path = os.path.join(IMAGES_DIR, f"scene_{scene_num}.jpg")

        # আগে থেকে ছবি থাকলে স্কিপ করবে (যাতে সময় বাঁচে)
        if os.path.exists(img_path):
            print(f"⏭️ Scene {scene_num} already exists. Skipping...")
            continue

        raw_prompt = scene.get('image_prompt', "A cute cartoon character")
        enhanced_prompt = f"3D Pixar style, masterpiece, highly detailed, vibrant colors, {raw_prompt}, wide angle shot, full body"
        encoded_prompt = urllib.parse.quote(enhanced_prompt)
        
        image_downloaded = False
        
        # 🌟 ম্যাজিক ট্রিক: ৩টি আলাদা মডেল দিয়ে অটো-রিট্রাই
        models = ['flux', 'turbo', 'default']
        
        for attempt in range(3):
            for model in models:
                try:
                    seed = random.randint(1, 1000000)
                    url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=1024&height=1024&nologo=true&model={model}&seed={seed}"
                    
                    print(f"🔄 Trying Pollinations ({model}) for Scene {scene_num}...")
                    
                    # 🌟 requests ব্যবহার করে কানেকশন স্ট্রং করা হলো
                    response = requests.get(url, timeout=60)
                    
                    if response.status_code == 200:
                        original_img = Image.open(BytesIO(response.content)).convert("RGB")
                        target_width, target_height = 1080, 1920
                        
                        fg_img = original_img.resize((1080, 1080))
                        bg_img = original_img.resize((target_width, target_height))
                        bg_img = bg_img.filter(ImageFilter.GaussianBlur(radius=35))
                        
                        y_offset = (target_height - 1080) // 2
                        bg_img.paste(fg_img, (0, y_offset))
                        
                        bg_img.save(img_path, "JPEG", quality=95)
                        
                        print(f"✅ Scene {scene_num} image saved successfully!")
                        image_downloaded = True
                        break
                    else:
                        print(f"⚠️ Server returned HTTP {response.status_code}. Switching model...")
                        
                except Exception as e:
                    print(f"⚠️ Request failed: {e}. Switching model...")
                    
            if image_downloaded:
                break
            else:
                print("⏳ All servers busy. Waiting 5s before retrying...")
                time.sleep(5)

        if not image_downloaded:
            print(f"❌ CRITICAL ERROR: Failed to generate image for Scene {scene_num}")
            images_success = False
            break

    return images_success
