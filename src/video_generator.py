import os
import json
import time
import requests
from deapi import DeapiClient
from config.settings import IMAGES_DIR, ANIMATED_DIR

def animate_scenes(story_path):
    token = os.environ.get("DEAPI_API_TOKEN")
    if not token:
        print("⚠️ DEAPI_API_TOKEN missing. Skipping animation rendering.")
        return

    client = DeapiClient(api_key=token)

    with open(story_path, 'r', encoding='utf-8') as f:
        story_data = json.load(f)

    for scene in story_data['scenes']:
        scene_num = scene['scene_number']
        img_path = os.path.join(IMAGES_DIR, f"scene_{scene_num}.jpg")
        vid_path = os.path.join(ANIMATED_DIR, f"scene_{scene_num}.mp4")

        if os.path.exists(img_path) and not os.path.exists(vid_path):
            print(f"🎬 Animating Scene {scene_num} using deAPI (Ltx2_19B)...")
            try:
                job = client.video.animate(
                    prompt="3d animated cartoon style, smooth camera movement, high quality fluid animation",
                    first_frame_image=img_path,
                    model="Ltx2_19B_Dist_FP8", # deAPI তে থাকা ভিডিও মডেল
                    seed=42,
                    width=1024,
                    height=576,
                    frames=120,
                    fps=24,
                )
                
                result = job.wait()
                
                res = requests.get(result.result_url)
                with open(vid_path, "wb") as f_out:
                    f_out.write(res.content)
                print(f"✅ Scene {scene_num} animation saved!")
            except Exception as e:
                print(f"❌ Error in scene {scene_num}: {e}")
            
            time.sleep(5)
