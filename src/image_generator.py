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

        # ছবি আগে থেকেই থাকলে নতুন করে বানাবে না
        if os.path.exists(img_path):
            continue

        prompt = scene.get('image_prompt', "3D Pixar style cartoon")
        # 9:16 পোর্ট্রেট স্টাইলের জন্য প্রম্পট
        enhanced_prompt = f"3D Pixar animation style, {prompt}, masterpiece, highly detailed, vibrant colors, beautiful lighting, FULL BODY SHOT, WIDE ANGLE, centered in frame, zoomed out, showing full environment"
        
        print(f"🎨 Generating Image for Scene {scene_num} using Free Backup API (Flux)...")

        image_downloaded = False
        encoded_prompt = urllib.parse.quote(enhanced_prompt)
        seed = random.randint(1, 1000000)
        
        # 1080x1920 (9:16 Shorts Ratio)
        image_url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=1080&height=1920&nologo=true&model=flux&seed={seed}"

        # API এরর এড়াতে ৩ বার চেষ্টা করবে
        for attempt in range(3):
            try:
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
