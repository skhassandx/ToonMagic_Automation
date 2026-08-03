import os
import sys

# সঠিক নামগুলো ইমপোর্ট করা হলো
from src.story_generator import generate_story
from src.image_generator import generate_images
from src.video_generator import animate_scenes
from src.video_editor import create_final_videos
from src.youtube_uploader import upload_to_youtube
from config.settings import STORY_JSON_PATH

def main():
    print("========================================")
    print("🚀 ToonMagic Bangla - Automated Pipeline")
    print("========================================")

    # 🛑 ফায়ারওয়াল ১: জেমিনাই চেক
    print("\n[Step 1] Loading Story...")
    story_generated = generate_story()
    
    if not story_generated:
        print("\n❌ CRITICAL ERROR: Gemini failed to generate a new story!")
        print("🛑 Pipeline Stopped: We will NOT upload a default/fake story to YouTube.")
        sys.exit(1) # স্ক্রিপ্ট বন্ধ

    # 🛑 ফায়ারওয়াল ২: ইমেজ চেক
    print("\n[Step 2] Generating AI Images...")
    images_status = generate_images(STORY_JSON_PATH)
    
    if not images_status:
        print("\n❌ CRITICAL ERROR: Image generation failed!")
        print("🛑 Pipeline Stopped: We will NOT upload a video without proper images.")
        sys.exit(1) # স্ক্রিপ্ট বন্ধ

    # 🎬 ভিডিও ক্লিপ জেনারেট (আপনার আসল ফাংশন কল করা হলো)
    print("\n[Step 3] Rendering Animation Scenes locally...")
    animate_scenes(STORY_JSON_PATH)

    # ✂️ ভিডিও এডিটিং ও মার্জিং
    print("\n[Step 4] Editing Video & Converting to 9:16 Shorts...")
    shorts_path = create_final_videos(STORY_JSON_PATH)

    if not shorts_path:
        print("\n❌ CRITICAL ERROR: Video rendering failed!")
        sys.exit(1)

    # 🚀 ইউটিউবে আপলোড
    print("\n[Step 5] Headless YouTube Uploading...")
    upload_status = upload_to_youtube(shorts_path, STORY_JSON_PATH)
    
    if upload_status:
        print("\n🎉 Pipeline Execution Completed Successfully!")
    else:
        print("\n⚠️ Video created, but YouTube Upload Failed.")

if __name__ == "__main__":
    main()
