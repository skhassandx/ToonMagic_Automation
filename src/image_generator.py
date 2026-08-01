import os
import json
import requests
from config.settings import IMAGES_DIR

def generate_images(story_path):
    token = os.environ.get("HF_API_TOKEN")
    if not token:
        print("⚠️ HF_API_TOKEN missing. Skipping image generation.")
        return

    # Hugging Face-এর সেরা ফ্রি ইমেজ মডেল (FLUX.1-schnell)
    API_URL = "https://api-inference.huggingface.co/models/black-forest-labs/FLUX.1-schnell"
    headers = {"Authorization": f"Bearer {token}"}

    with open(story_path, 'r', encoding='utf-8') as f:
        story_data = json.load(f)

    for scene in story_data['scenes']:
        scene_num = scene['scene_number']
        img_path = os.path.join(IMAGES_DIR, f"scene_{scene_num}.jpg")

        if not os.path.exists(img_path):
            print(f"🎨 Generating Image for Scene {scene_num} via Hugging Face...")
            try:
                payload = {
                    "inputs": "3D Pixar style cartoon animation scene, cute boy named Tutul, magical glowing pencil, vibrant colors, highly detailed",
                    "parameters": {"width": 1024, "height": 576}
                }
                
                response = requests.post(API_URL, headers=headers, json=payload)
                
                if response.status_code == 200:
                    with open(img_path, "wb") as f_img:
                        f_img.write(response.content)
                    print(f"✅ Scene {scene_num} image generated successfully!")
                else:
                    print(f"❌ Error generating image for scene {scene_num}. Status Code: {response.status_code}")
                    print(f"Response: {response.text}")
            except Exception as e:
                print(f"❌ Error: {e}")
