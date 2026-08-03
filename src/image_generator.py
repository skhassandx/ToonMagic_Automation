import os
import json
import time
import requests
import urllib.request
import urllib.parse
import random
from config.settings import IMAGES_DIR

def generate_images(story_path):
    with open(story_path, 'r', encoding='utf-8') as f:
        story_data = json.load(f)

    # আপনার গিটহাবের সিক্রেট নাম অনুযায়ী HF_API_TOKEN সেট করা হলো
    hf_api_key = os.environ.get("HF_API_TOKEN")
    
    # 3D Pixar স্টাইলের জন্য Stable Diffusion XL মডেল
    API_URL = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-xl-base-1.0"
    headers = {"Authorization": f"Bearer {hf_api_key}"} if hf_api_key else {}

    images_success = True

    for scene in story_data['scenes']:
        scene_num = scene['scene_number']
        img_path = os.path.join(IMAGES_DIR, f"scene_{scene_num}.jpg")

        if os.path.exists(img_path):
            continue

        print(f"🎨 Generating Ultra-HD Image for Scene {scene_num}...")
        prompt = scene.get('image_prompt', "3D Pixar style, cute cartoon character")
        enhanced_prompt = f"3D Pixar animation style, {prompt}, masterpiece, highly detailed, 8k resolution, cinematic lighting, vibrant colors"

        image_downloaded = False

        # ১. প্রথমে Hugging Face API দিয়ে সেরা কোয়ালিটির ছবি বানানোর চেষ্টা
        if hf_api_key:
            print(f"🤗 Requesting Hugging Face API for Scene {scene_num}...")
            payload = {"inputs": enhanced_prompt}
            
            for attempt in range(3):
                try:
                    response = requests.post(API_URL, headers=headers, json=payload, timeout=60)
                    if response.status_code == 200:
                        with open(img_path, 'wb') as f_img:
                            f_img.write(response.content)
                        print(f"✅ Scene {scene_num} generated with Hugging Face!")
                        image_downloaded = True
                        break
                    else:
                        print(f"⏳ Hugging Face model loading (Attempt {attempt+1}): {response.json()}")
                        time.sleep(15)
                except Exception as e:
                    print(f"⚠️ Hugging Face Error: {e}")
                    time.sleep(5)

        # ২. Hugging Face ফেইল করলে আমাদের সেফটি ফলব্যাক (Flux) কাজ করবে
        if not image_downloaded:
            print(f"🔄 Switching to Backup (Flux) for Scene {scene_num}...")
            encoded_prompt = urllib.parse.quote(enhanced_prompt)
            seed = random.randint(1, 1000000)
            image_url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=1080&height=1920&nologo=true&model=flux&seed={seed}"
            
            for attempt in range(3):
                try:
                    req = urllib.request.Request(image_url, headers={'User-Agent': 'Mozilla/5.0'})
                    with urllib.request.urlopen(req, timeout=60) as res, open(img_path, 'wb') as out_file:
                        out_file.write(res.read())
                    print(f"✅ Scene {scene_num} generated via Flux Backup!")
                    image_downloaded = True
                    break
                except Exception as e:
                    print(f"⚠️ Flux Error on attempt {attempt+1}: {e}")
                    time.sleep(3)
                    
        if not image_downloaded:
            images_success = False
            print(f"❌ CRITICAL ERROR: Failed to generate image for Scene {scene_num}")
            break

    return images_success
