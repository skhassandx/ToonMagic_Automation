import os
import sys

from src.story_generator import generate_story
from src.image_generator import generate_images
from src.video_generator import animate_scenes
from src.video_editor import create_final_videos
from src.youtube_uploader import upload_to_youtube_headless
from config.settings import STORY_JSON_PATH

def main():
    print("========================================")
    print("🚀 ToonMagic Bangla - Automated Pipeline")
    print("========================================")

    print("\n[Step 1] Loading Story...")
    story_generated = generate_story()
    
    if not story_generated:
        print("\n❌ CRITICAL ERROR: Gemini failed to generate a new story!")
        sys.exit(1)

    print("\n[Step 2] Generating AI Images...")
    images_status = generate_images(STORY_JSON_PATH)
    
    if not images_status:
        print("\n❌ CRITICAL ERROR: Image generation failed!")
        sys.exit(1)

    print("\n[Step 3] Rendering Animation Scenes locally...")
    animate_scenes(STORY_JSON_PATH)

    print("\n[Step 4] Editing Video & Converting to 9:16 Shorts...")
    # create_final_videos দুটি ভ্যালু রিটার্ন করে, তাই আমরা প্রথমটি (shorts_path) নিচ্ছি
    shorts_path, _ = create_final_videos(STORY_JSON_PATH)

    if not shorts_path:
        print("\n❌ CRITICAL ERROR: Video rendering failed!")
        sys.exit(1)

    print("\n[Step 5] Headless YouTube Uploading...")
    # ফাংশনের সঠিক নাম এবং শুধু একটি আর্গুমেন্ট পাঠানো হলো
    upload_status = upload_to_youtube_headless(shorts_path)
    
    if upload_status:
        print("\n🎉 Pipeline Execution Completed Successfully!")
    else:
        print("\n⚠️ Video created, but YouTube Upload Failed.")

if __name__ == "__main__":
    main()
