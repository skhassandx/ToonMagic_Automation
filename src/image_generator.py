import os
import json
import time
import urllib.request
import urllib.parse
import random
from io import BytesIO
from PIL import Image, ImageFilter
from config.settings import IMAGES_DIR

def generate_images(story_path):
    print("🎨 Generating Images (Square 1024x1024 + Cinematic Blur) with Fallback...")
    with open(story_path, 'r', encoding='utf-8') as f:
        story_data = json.load(f)

    images_success = True

    # 🌟 ম্যাজিক ট্রিক: ইমেজের জন্যও ফলব্যাক মডেল যুক্ত করা হলো
    image_models_to_try = ['flux', 'turbo', 'default']

    for scene in story_data['scenes']:
        scene_num = scene['scene_number']
        img_path = os.path.join(IMAGES_DIR, f"scene_{scene_num}.jpg")

        if os.path.exists(img_path):
            continue

        prompt = scene.get('image_prompt', "3D Pixar style scene")
        enhanced_prompt = f"3D Pixar animation style, {prompt}, masterpiece, highly detailed, vibrant colors, full body character visible"
        encoded_prompt = urllib.parse.quote(enhanced_prompt)
        seed = random.randint(1, 1000000)

        image_downloaded = False
        
        for attempt in range(3):
            for model_name in image_models_to_try:
                try:
                    print(f"🔄 Trying image model: {model_name} for Scene {scene_num}...")
                    image_url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=1024&height=1024&nologo=true&model={model_name}&seed={seed}"
                    
                    req = urllib.request.Request(image_url, headers={'User-Agent': 'Mozilla/5.0'})
                    with urllib.request.urlopen(req, timeout=60) as res:
                        img_data = res.read()
                        
                        original_img = Image.open(BytesIO(img_data)).convert("RGB")
                        target_width, target_height = 1080, 1920
                        
                        bg_img = original_img.resize((target_width, target_height))
                        bg_img = bg_img.filter(ImageFilter.GaussianBlur(radius=35))
                        
                        fg_img = original_img.resize((target_width, target_width))
                        y_offset = (target_height - target_width) // 2
                        bg_img.paste(fg_img, (0, y_offset))
                        
                        bg_img.save(img_path, "JPEG", quality=95)
                        
                    print(f"✅ Scene {scene_num} image generated successfully with {model_name}!")
                    image_downloaded = True
                    break # সফল হলে এই সিনের লুপ ভেঙে পরের সিনে যাবে
                
                except Exception as e:
                    print(f"⚠️ {model_name} failed: {e}")
                    print("⏳ Switching to next fallback model...")
                    time.sleep(3)
            
            if image_downloaded:
                break # সফল হলে attempt লুপ ভাঙবে

        if not image_downloaded:
            print(f"❌ CRITICAL ERROR: All models failed for Scene {scene_num}")
            images_success = False
            break

    return images_success
