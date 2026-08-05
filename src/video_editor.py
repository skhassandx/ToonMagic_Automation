import os
import json
from moviepy.editor import ImageClip, AudioFileClip, concatenate_videoclips
from config.settings import IMAGES_DIR, AUDIO_DIR, OUTPUT_DIR

def create_video(story_path):
    print("🎬 Assembling Short Video with Fast Transitions...")
    with open(story_path, 'r', encoding='utf-8') as f:
        story_data = json.load(f)

    clips = []

    for scene in story_data['scenes']:
        scene_num = scene['scene_number']
        img_path = os.path.join(IMAGES_DIR, f"scene_{scene_num}.jpg")
        audio_path = os.path.join(AUDIO_DIR, f"scene_{scene_num}.mp3")

        if not os.path.exists(img_path) or not os.path.exists(audio_path):
            print(f"❌ Missing assets for Scene {scene_num}")
            return False

        audio_clip = AudioFileClip(audio_path)
        # ছবিটিকে অডিওর দৈর্ঘ্যের সমান করে ক্লিপ তৈরি
        img_clip = ImageClip(img_path).set_duration(audio_clip.duration)
        img_clip = img_clip.set_audio(audio_clip)

        clips.append(img_clip)

    final_video = concatenate_videoclips(clips, method="compose")
    output_video_path = os.path.join(OUTPUT_DIR, "final_shorts.mp4")

    # 🌟 শর্টস ভিডিও রেন্ডার
    final_video.write_videofile(
        output_video_path,
        fps=24,
        codec="libx264",
        audio_codec="aac",
        preset="ultrafast"
    )

    print(f"✅ Video generated successfully: {output_video_path}")
    return output_video_path
