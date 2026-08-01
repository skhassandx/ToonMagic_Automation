import os
import json
import requests
import replicate
from config.settings import IMAGES_DIR

def generate_images(story_path):
    token = os.environ.get("REPLICATE_API_TOKEN")
    if not token:
        print("⚠️ REPLICATE_API_TOKEN missing. Skipping image generation.")
        return

    os.environ["REPLICATE_API_TOKEN"] = token

    with open(story_path, 'r', encoding='utf-8') as f:
        story_data = json.load(f)

    for scene in story_data['scenes']:
        scene_num = scene['scene_number']
        img_path = os.path.join(IMAGES_DIR, f"scene_{scene_num}.jpg")

        if not os.path.exists(img_path):
            print(f"🎨 Generating Image for Scene {scene_num}...")
            try:
                # প্রম্পট: 3D Pixar style
                prompt_en = "3D Pixar style cartoon animation scene, cute boy named Tutul, magical glowing pencil, vibrant colors, highly detailed"
                output_img = replicate.run(
                    "black-forest-labs/flux-schnell",
                    input={"prompt": prompt_en, "aspect_ratio": "16:9"}
                )
                img_url = output_img[0] if isinstance(output_img, list) else str(output_img)
                res_img = requests.get(img_url)
                with open(img_path, "wb") as f_img:
                    f_img.write(res_img.content)
                print(f"✅ Scene {scene_num} image generated successfully!")
            except Exception as e:
                print(f"❌ Error generating image for scene {scene_num}: {e}")
