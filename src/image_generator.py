import os
import json
import urllib.request
import urllib.parse
import time
from config.settings import IMAGES_DIR

def generate_images(story_path):
    # কোনো API Token লাগবে না!

    with open(story_path, 'r', encoding='utf-8') as f:
        story_data = json.load(f)

    for scene in story_data['scenes']:
        scene_num = scene['scene_number']
        img_path = os.path.join(IMAGES_DIR, f"scene_{scene_num}.jpg")

        if not os.path.exists(img_path):
            print(f"🎨 Generating Image for Scene {scene_num} via Pollinations AI...")
            
            prompt = f"3D Pixar style cartoon animation scene, highly detailed, vibrant colors, scene number {scene_num}"
            encoded_prompt = urllib.parse.quote(prompt)
            # Pollinations AI Endpoint (Free & No Token Required)
            image_url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=1024&height=576&nologo=true"
            
            max_retries = 3
            for attempt in range(max_retries):
                try:
                    req = urllib.request.Request(image_url, headers={'User-Agent': 'Mozilla/5.0'})
                    with urllib.request.urlopen(req, timeout=60) as response, open(img_path, 'wb') as out_file:
                        out_file.write(response.read())
                    print(f"✅ Scene {scene_num} image generated successfully!")
                    time.sleep(2) # সার্ভারে চাপ কমানোর জন্য একটু বিরতি
                    break
                except Exception as e:
                    print(f"⚠️ Error on attempt {attempt+1}: {e}")
                    if attempt < max_retries - 1:
                        print("🔄 Retrying in 5 seconds...")
                        time.sleep(5)
                    else:
                        print(f"❌ Failed to generate image for scene {scene_num}.")
