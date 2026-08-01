import os
import json
import requests
from deapi import DeapiClient
from config.settings import IMAGES_DIR

def generate_images(story_path):
    token = os.environ.get("DEAPI_API_TOKEN")
    if not token:
        print("⚠️ DEAPI_API_TOKEN missing. Skipping image generation.")
        return

    client = DeapiClient(api_key=token)

    with open(story_path, 'r', encoding='utf-8') as f:
        story_data = json.load(f)

    for scene in story_data['scenes']:
        scene_num = scene['scene_number']
        img_path = os.path.join(IMAGES_DIR, f"scene_{scene_num}.jpg")

        if not os.path.exists(img_path):
            print(f"🎨 Generating Image for Scene {scene_num} via deAPI...")
            try:
                # প্রম্পট: 3D Pixar style
                prompt_en = "3D Pixar style cartoon animation scene, cute boy named Tutul, magical glowing pencil, vibrant colors, highly detailed"
                
                job = client.images.generate(
                    prompt=prompt_en,
                    model="Flux1schnell", # deAPI তে থাকা ফ্লাক্স মডেল
                    width=1024,
                    height=576, # 16:9 ratio
                    seed=42,
                )
                
                result = job.wait()
                
                res_img = requests.get(result.result_url)
                with open(img_path, "wb") as f_img:
                    f_img.write(res_img.content)
                print(f"✅ Scene {scene_num} image generated successfully!")
            except Exception as e:
                print(f"❌ Error generating image for scene {scene_num}: {e}")
