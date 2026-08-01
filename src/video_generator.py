import os
import json
from moviepy.editor import ImageClip
from config.settings import IMAGES_DIR, ANIMATED_DIR

def animate_scenes(story_path):
    # কোনো পেইড API ছাড়াই গিটহাব নিজেই ছবিকে ভিডিও বানাবে
    with open(story_path, 'r', encoding='utf-8') as f:
        story_data = json.load(f)

    for scene in story_data['scenes']:
        scene_num = scene['scene_number']
        img_path = os.path.join(IMAGES_DIR, f"scene_{scene_num}.jpg")
        vid_path = os.path.join(ANIMATED_DIR, f"scene_{scene_num}.mp4")

        if os.path.exists(img_path) and not os.path.exists(vid_path):
            print(f"🎬 Creating Video for Scene {scene_num} locally...")
            try:
                # ছবি থেকে ৫ সেকেন্ডের ভিডিও ক্লিপ তৈরি
                clip = ImageClip(img_path).set_duration(5)
                clip.write_videofile(vid_path, fps=24, codec="libx264", audio=False, verbose=False, logger=None)
                print(f"✅ Scene {scene_num} video saved!")
            except Exception as e:
                print(f"❌ Error in scene {scene_num}: {e}")
