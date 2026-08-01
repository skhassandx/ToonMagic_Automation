import os
import json
import urllib.request
import urllib.parse
import time
import random
from config.settings import IMAGES_DIR

def generate_images(story_path):
    with open(story_path, 'r', encoding='utf-8') as f:
        story_data = json.load(f)

    for scene in story_data['scenes']:
        scene_num = scene['scene_number']
        img_path = os.path.join(IMAGES_DIR, f"scene_{scene_num}.jpg")

        if not os.path.exists(img_path):
            print(f"🎨 Generating Image for Scene {scene_num}...")
            
            prompt = scene.get('image_prompt', "Vertical 9:16 format, 3D Pixar style cartoon scene")
            encoded_prompt = urllib.parse.quote(prompt)
            seed = random.randint(1, 1000000)
            
            # Width ও Height পরিবর্তন করে 9:16 (Shorts) করা হয়েছে
            image_url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=576&height=1024&nologo=true&seed={seed}"
            
            for attempt in range(3):
                try:
                    req = urllib.request.Request(image_url, headers={'User-Agent': 'Mozilla/5.0'})
                    with urllib.request.urlopen(req, timeout=60) as response, open(img_path, 'wb') as out_file:
                        out_file.write(response.read())
                    print(f"✅ Scene {scene_num} image generated successfully!")
                    time.sleep(2)
                    break
                except Exception as e:
                    print(f"⚠️ Error on attempt {attempt+1}: {e}")
                    time.sleep(5)
