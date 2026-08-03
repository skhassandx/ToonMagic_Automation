import os
import sys

from src.story_generator import generate_story
from src.image_generator import generate_images
from src.audio_generator import generate_audio  # 🌟 অডিও ইমপোর্ট করা হলো
from src.video_generator import animate_scenes
from src.video_editor import create_final_videos
from src.youtube_uploader import upload_to_youtube_headless
from config.settings import STORY_JSON_PATH

def main():
    print("========================================")
    print("🚀 ToonMagic Bangla - Automated Pipeline")
    print("========================================")

    print("\n[Step 1] Loading Story...")
    if not generate_story():
        sys.exit(1)

    print("\n[Step 2] Generating Audio Voiceover...")
    generate_audio(STORY_JSON_PATH)  # 🌟 অডিও জেনারেট হচ্ছে

    print("\n[Step 3] Generating AI Images...")
    if not generate_images(STORY_JSON_PATH):
        sys.exit(1)

    print("\n[Step 4] Rendering Animation Scenes locally...")
    animate_scenes(STORY_JSON_PATH)

    print("\n[Step 5] Editing Video & Converting to 9:16 Shorts...")
    shorts_path, _ = create_final_videos(STORY_JSON_PATH)
    if not shorts_path:
        sys.exit(1)

    print("\n[Step 6] Headless YouTube Uploading...")
    upload_status = upload_to_youtube_headless(shorts_path)
    
    if upload_status:
        print("\n🎉 Pipeline Execution Completed Successfully!")
    else:
        print("\n⚠️ YouTube Upload Failed.")

if __name__ == "__main__":
    main()
