import os
import json
import requests
import time
from config.settings import IMAGES_DIR

def generate_images(story_path):
    token = os.environ.get("DEAPI_API_TOKEN")
    if not token:
        print("⚠️ DEAPI_API_TOKEN missing. Skipping image generation.")
        return

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    with open(story_path, 'r', encoding='utf-8') as f:
        story_data = json.load(f)

    for scene in story_data['scenes']:
        scene_num = scene['scene_number']
        img_path = os.path.join(IMAGES_DIR, f"scene_{scene_num}.jpg")

        if not os.path.exists(img_path):
            print(f"🎨 Generating Image for Scene {scene_num} via deAPI...")
            try:
                payload = {
                    "prompt": "3D Pixar style cartoon animation scene, cute boy named Tutul, magical glowing pencil, vibrant colors, highly detailed",
                    "model": "Flux1schnell",
                    "width": 1024,
                    "height": 576,
                    "seed": 42
                }
                
                # ১. জব সাবমিট করা
                res = requests.post("https://api.deapi.ai/v1/images/generations", json=payload, headers=headers)
                job_data = res.json()
                
                if "id" not in job_data:
                    print(f"❌ API Error: {job_data}")
                    continue
                    
                job_id = job_data["id"]
                print(f"⏳ Job created: {job_id}. Waiting for completion...")
                
                # ২. রেজাল্ট পাওয়া পর্যন্ত চেক করা
                result_url = None
                for _ in range(30): # সর্বোচ্চ ৫ মিনিট অপেক্ষা করবে
                    time.sleep(10)
                    poll_res = requests.get(f"https://api.deapi.ai/v1/jobs/{job_id}", headers=headers)
                    poll_data = poll_res.json()
                    
                    if poll_data.get("status") == "succeeded":
                        result_url = poll_data.get("result_url")
                        break
                    elif poll_data.get("status") == "failed":
                        print("❌ Image generation failed on server.")
                        break

                if result_url:
                    img_res = requests.get(result_url)
                    with open(img_path, "wb") as f_img:
                        f_img.write(img_res.content)
                    print(f"✅ Scene {scene_num} image generated successfully!")
            except Exception as e:
                print(f"❌ Error generating image for scene {scene_num}: {e}")
