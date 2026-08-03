import os
import json
import requests
import time
import urllib.request
import urllib.parse
import random
from config.settings import IMAGES_DIR

def generate_images(story_path):
    with open(story_path, 'r', encoding='utf-8') as f:
        story_data = json.load(f)

    leonardo_api_key = os.environ.get("LEONARDO_API_KEY")

    for scene in story_data['scenes']:
        scene_num = scene['scene_number']
        img_path = os.path.join(IMAGES_DIR, f"scene_{scene_num}.jpg")

        if os.path.exists(img_path):
            continue

        print(f"🎨 Generating Image for Scene {scene_num}...")
        prompt = scene.get('image_prompt', "Vertical 9:16 format, 3D Pixar style cartoon scene, highly detailed")
        enhanced_prompt = f"{prompt}, 3D Pixar animation style, masterpiece, highly detailed, 8k resolution, vibrant colors"

        image_downloaded = False

        # ১. চেষ্টা করবে Leonardo AI API দিয়ে প্রিমিয়াম ৩ডি ছবি বানাতে
        if leonardo_api_key:
            try:
                print(f"🦁 Requesting Leonardo AI for Scene {scene_num}...")
                headers = {
                    "accept": "application/json",
                    "content-type": "application/json",
                    "authorization": f"Bearer {leonardo_api_key}"
                }
                payload = {
                    "height": 1024,
                    "width": 576, # 9:16 Vertical Aspect Ratio
                    "modelId": "e71a1c2c-4f77-4107-96c8-f8608298711e", # 3D Animation Style Model
                    "prompt": enhanced_prompt,
                    "num_images": 1
                }
                response = requests.post("https://cloud.leonardo.ai/api/rest/v1/generations", json=payload, headers=headers)
                data = response.json()

                if "sdGenerationJob" in data:
                    generation_id = data["sdGenerationJob"]["generationId"]
                    
                    # ছবি তৈরি হওয়া পর্যন্ত অপেক্ষা
                    for _ in range(12): 
                        time.sleep(5)
                        gen_res = requests.get(f"https://cloud.leonardo.ai/api/rest/v1/generations/{generation_id}", headers=headers)
                        gen_data = gen_res.json()
                        
                        images = gen_data.get("generations_by_pk", {}).get("generated_images", [])
                        if images and len(images) > 0:
                            img_url = images[0]["url"]
                            img_data = requests.get(img_url).content
                            with open(img_path, 'wb') as handler:
                                handler.write(img_data)
                            print(f"✅ Scene {scene_num} generated with Leonardo AI!")
                            image_downloaded = True
                            break
            except Exception as e:
                print(f"⚠️ Leonardo AI Error: {e}. Falling back to Flux...")

        # ২. যদি লিওনার্দো ক্রেডিট শেষ হয়ে যায় বা কোনো সমস্যা হয়, অটোমেটিক ফ্রি Flux থেকে ছবি বানাবে
        if not image_downloaded:
            encoded_prompt = urllib.parse.quote(enhanced_prompt)
            seed = random.randint(1, 1000000)
            image_url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=1080&height=1920&nologo=true&model=flux&seed={seed}"
            
            for attempt in range(3):
                try:
                    req = urllib.request.Request(image_url, headers={'User-Agent': 'Mozilla/5.0'})
                    with urllib.request.urlopen(req, timeout=60) as res, open(img_path, 'wb') as out_file:
                        out_file.write(res.read())
                    print(f"✅ Scene {scene_num} generated via Flux (Backup)!")
                    break
                except Exception as e:
                    print(f"⚠️ Flux Error on attempt {attempt+1}: {e}")
                    time.sleep(3)
