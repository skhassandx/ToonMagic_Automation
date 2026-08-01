import os
import json
import time
import requests
import replicate
from config.settings import IMAGES_DIR, ANIMATED_DIR

def animate_scenes(story_path):
    token = os.environ.get("REPLICATE_API_TOKEN")
    if not token:
        print("⚠️ REPLICATE_API_TOKEN missing. Skipping animation rendering.")
        return

    os.environ["REPLICATE_API_TOKEN"] = token

    with open(story_path, 'r', encoding='utf-8') as f:
        story_data = json.load(f)

    for scene in story_data['scenes']:
        scene_num = scene['scene_number']
        img_path = os.path.join(IMAGES_DIR, f"scene_{scene_num}.jpg")
        vid_path = os.path.join(ANIMATED_DIR, f"scene_{scene_num}.mp4")

        if os.path.exists(img_path) and not os.path.exists(vid_path):
            print(f"🎬 Animating Scene {scene_num} using Minimax...")
            try:
                with open(img_path, "rb") as input_file:
                    output = replicate.run(
                        "minimax/video-01",
                        input={
                            "first_frame_image": input_file,
                            "prompt": "3d animated cartoon style, smooth camera movement, high quality fluid animation"
                        }
                    )
                vid_url = output[0] if isinstance(output, list) else str(output)
                res = requests.get(vid_url)
                with open(vid_path, "wb") as f_out:
                    f_out.write(res.content)
                print(f"✅ Scene {scene_num} animation saved!")
            except Exception as e:
                print(f"❌ Error in scene {scene_num}: {e}")
            
            time.sleep(10)
