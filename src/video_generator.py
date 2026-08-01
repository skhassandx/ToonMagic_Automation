import os
import json
import time
import requests
from config.settings import IMAGES_DIR, ANIMATED_DIR
import base64

def get_base64_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

def animate_scenes(story_path):
    token = os.environ.get("DEAPI_API_TOKEN")
    if not token:
        print("⚠️ DEAPI_API_TOKEN missing. Skipping animation rendering.")
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
        vid_path = os.path.join(ANIMATED_DIR, f"scene_{scene_num}.mp4")

        if os.path.exists(img_path) and not os.path.exists(vid_path):
            print(f"🎬 Animating Scene {scene_num} using deAPI (Ltx2_19B)...")
            try:
                base64_img = get_base64_image(img_path)
                
                payload = {
                    "prompt": "3d animated cartoon style, smooth camera movement, high quality fluid animation",
                    "model": "Ltx2_19B_Dist_FP8",
                    "first_frame_image": f"data:image/jpeg;base64,{base64_img}",
                    "width": 1024,
                    "height": 576,
                    "frames": 120,
                    "fps": 24,
                    "seed": 42
                }
                
                # ১. জব সাবমিট করা
                res = requests.post("https://api.deapi.ai/v1/videos/generations", json=payload, headers=headers)
                job_data = res.json()
                
                if "id" not in job_data:
                    print(f"❌ API Error: {job_data}")
                    continue
                    
                job_id = job_data["id"]
                print(f"⏳ Job created: {job_id}. Waiting for completion...")
                
                # ২. রেজাল্ট পাওয়া পর্যন্ত চেক করা
                result_url = None
                for _ in range(60): # সর্বোচ্চ ১০ মিনিট অপেক্ষা করবে
                    time.sleep(10)
                    poll_res = requests.get(f"https://api.deapi.ai/v1/jobs/{job_id}", headers=headers)
                    poll_data = poll_res.json()
                    
                    if poll_data.get("status") == "succeeded":
                        result_url = poll_data.get("result_url")
                        break
                    elif poll_data.get("status") == "failed":
                        print("❌ Video generation failed on server.")
                        break

                if result_url:
                    vid_res = requests.get(result_url)
                    with open(vid_path, "wb") as f_out:
                        f_out.write(vid_res.content)
                    print(f"✅ Scene {scene_num} animation saved!")
            except Exception as e:
                print(f"❌ Error in scene {scene_num}: {e}")
            
            time.sleep(5)
