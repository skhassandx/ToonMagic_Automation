import os
import json
import requests
import time
from config.settings import IMAGES_DIR

def generate_images(story_path):
    token = os.environ.get("HF_API_TOKEN")
    if not token:
        print("⚠️ HF_API_TOKEN missing. Skipping image generation.")
        return

    API_URL = "https://api-inference.huggingface.co/models/black-forest-labs/FLUX.1-schnell"
    headers = {"Authorization": f"Bearer {token}"}

    with open(story_path, 'r', encoding='utf-8') as f:
        story_data = json.load(f)

    for scene in story_data['scenes']:
        scene_num = scene['scene_number']
        img_path = os.path.join(IMAGES_DIR, f"scene_{scene_num}.jpg")

        if not os.path.exists(img_path):
            print(f"🎨 Generating Image for Scene {scene_num} via Hugging Face...")
            
            # নেটওয়ার্ক ড্রপ করলে ৩ বার চেষ্টা করবে
            max_retries = 3
            for attempt in range(max_retries):
                try:
                    payload = {
                        "inputs": "3D Pixar style cartoon animation scene, cute boy named Tutul, magical glowing pencil, vibrant colors, highly detailed",
                        "parameters": {"width": 1024, "height": 576}
                    }
                    
                    response = requests.post(API_URL, headers=headers, json=payload, timeout=60)
                    
                    if response.status_code == 200:
                        with open(img_path, "wb") as f_img:
                            f_img.write(response.content)
                        print(f"✅ Scene {scene_num} image generated successfully!")
                        break # সফল হলে লুপ থেকে বেরিয়ে যাবে
                    elif response.status_code == 503:
                        print(f"⏳ Server is busy/loading. Retrying in 20 seconds... (Attempt {attempt+1}/{max_retries})")
                        time.sleep(20)
                    else:
                        print(f"❌ API Error {response.status_code}: {response.text}")
                        break
                        
                except requests.exceptions.RequestException as e:
                    print(f"⚠️ Network error on attempt {attempt+1}: {e}")
                    if attempt < max_retries - 1:
                        print("🔄 Retrying in 10 seconds...")
                        time.sleep(10)
                    else:
                        print("❌ Failed to connect after multiple attempts.")
