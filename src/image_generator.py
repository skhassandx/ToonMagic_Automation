import os
import json
import time
import requests
from config.settings import IMAGES_DIR

def generate_images(story_path):
    with open(story_path, 'r', encoding='utf-8') as f:
        story_data = json.load(f)

    # Hugging Face API Key
    api_key = os.environ.get("HF_API_KEY")
    if not api_key:
        print("❌ CRITICAL ERROR: HF_API_KEY not found in environment variables!")
        return False

    images_success = True
    # Stable Diffusion XL Model
    API_URL = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-xl-base-1.0"
    headers = {"Authorization": f"Bearer {api_key}"}

    for scene in story_data['scenes']:
        scene_num = scene['scene_number']
        img_path = os.path.join(IMAGES_DIR, f"scene_{scene_num}.jpg")

        if os.path.exists(img_path):
            continue

        prompt = scene.get('image_prompt', "A cartoon bear")
        # প্রফেশনাল প্রম্পট
        enhanced_prompt = f"3D Pixar style, highly detailed, {prompt}, wide angle shot, full body, cinematic lighting, 8k resolution"
        
        print(f"🎨 Generating Image for Scene {scene_num} using Hugging Face (SDXL)...")

        image_downloaded = False
        
        for attempt in range(3):
            try:
                response = requests.post(API_URL, headers=headers, json={"inputs": enhanced_prompt})
                if response.status_code == 200:
                    with open(img_path, 'wb') as out_file:
                        out_file.write(response.content)
                    print(f"✅ Scene {scene_num} image saved successfully!")
                    image_downloaded = True
                    break
                else:
                    print(f"⚠️ API returned status {response.status_code}. Retrying...")
                    time.sleep(10) # মডেল লোড হতে সময় লাগতে পারে
            except Exception as e:
                print(f"⚠️ Image generation failed on attempt {attempt+1}: {e}")
                time.sleep(5)

        if not image_downloaded:
            print(f"❌ CRITICAL ERROR: Failed to generate image for Scene {scene_num}")
            images_success = False
            break

    return images_success
