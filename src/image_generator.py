import os
import json
import time
import urllib.request
import urllib.parse
import random
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

        prompt = scene.get('image_prompt', "A cartoon character")
        
        # 🌟 ম্যাজিক প্রম্পট: ক্যারেক্টার যেন একদম সেন্টারে এবং ফুল বডি থাকে
        enhanced_prompt = f"3D Pixar style, masterpiece, highly detailed, FULL BODY WIDE SHOT, {prompt}, character is fully visible, beautiful background"
        
        print(f"🎨 Generating Image for Scene {scene_num} using Unlimited Free API (Pollinations)...")

        encoded_prompt = urllib.parse.quote(enhanced_prompt)
        seed = random.randint(1, 1000000)
        
        # 🌟 সাইজ ফিক্স: ৭৬৮x১০২৪ (AI এই সাইজে জুম-ইন না করে ফুল বডি রেন্ডার করে)
        image_url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=768&height=1024&nologo=true&model=flux&seed={seed}"

        image_downloaded = False
        
        for attempt in range(3):
            try:
                # কোনো API Key লাগবে না, কোনো 402 Error আসবে না!
                req = urllib.request.Request(image_url, headers={'User-Agent': 'Mozilla/5.0'})
                with urllib.request.urlopen(req, timeout=60) as res, open(img_path, 'wb') as out_file:
                    out_file.write(res.read())
                print(f"✅ Scene {scene_num} image saved successfully!")
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
