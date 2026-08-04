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
    with open(story_path, 'r', encoding='utf-8') as f:
        story_data = json.load(f)

    images_success = True

    for scene in story_data['scenes']:
        scene_num = scene['scene_number']
        img_path = os.path.join(IMAGES_DIR, f"scene_{scene_num}.jpg")

        if os.path.exists(img_path):
            continue

        prompt = scene.get('image_prompt', "A cartoon scene")
        
        # 🌟 ম্যাজিক প্রম্পট: স্কয়ার ছবির জন্য পারফেক্ট নির্দেশ
        enhanced_prompt = f"3D Pixar animation style, {prompt}, masterpiece, highly detailed, colorful, wide landscape, full body character visible"
        
        print(f"🎨 Generating Image for Scene {scene_num} using Pollinations (Square + Blur Padding)...")

        encoded_prompt = urllib.parse.quote(enhanced_prompt)
        seed = random.randint(1, 1000000)
        
        # 🌟 এআই-কে স্কয়ার (১০২৪x১০২৪) ছবি বানাতে বলা হচ্ছে, যাতে সে ক্রপ না করে
        image_url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=1024&height=1024&nologo=true&model=flux&seed={seed}"

        image_downloaded = False
        
        for attempt in range(3):
            try:
                req = urllib.request.Request(image_url, headers={'User-Agent': 'Mozilla/5.0'})
                with urllib.request.urlopen(req, timeout=60) as res:
                    img_data = res.read()
                    
                    # 🌟 পাইথন দিয়ে ছবিটিকে শর্টস (৯:১৬) ফরম্যাটে ব্লার ব্যাকগ্রাউন্ডসহ সাজানো হচ্ছে
                    original_img = Image.open(BytesIO(img_data)).convert("RGB")
                    
                    target_width, target_height = 1080, 1920
                    
                    # ১. ব্যাকগ্রাউন্ডের জন্য ছবিটিকে বড় করে ব্লার করা
                    bg_img = original_img.resize((target_width, target_height))
                    bg_img = bg_img.filter(ImageFilter.GaussianBlur(radius=35))
                    
                    # ২. আসল ছবিটিকে স্ক্রিনের সাইজ অনুযায়ী রিসাইজ করা
                    fg_img = original_img.resize((target_width, target_width))
                    
                    # ৩. ব্লার ব্যাকগ্রাউন্ডের ঠিক মাঝখানে আসল ছবিটি বসানো
                    y_offset = (target_height - target_width) // 2
                    bg_img.paste(fg_img, (0, y_offset))
                    
                    # চূড়ান্ত ছবি সেভ করা
                    bg_img.save(img_path, "JPEG", quality=95)
                    
                print(f"✅ Scene {scene_num} image saved successfully (No Crop!)")
                image_downloaded = True
                break
            except Exception as e:
                print(f"⚠️ Image generation failed on attempt {attempt+1}: {e}")
                time.sleep(5)

        if not image_downloaded:
            print(f"❌ CRITICAL ERROR: Failed to generate image for Scene {scene_num}")
            images_success = False
            break

    return images_success
