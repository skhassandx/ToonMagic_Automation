import os
import sys
from story_generator import generate_story
from video_generator import generate_audio
from image_generator import generate_images
from video_editor import create_final_videos
from youtube_uploader import upload_to_youtube
from config.settings import STORY_JSON_PATH

def main():
    print("========================================")
    print("🚀 ToonMagic Bangla - Automated Pipeline")
    print("========================================")

    # 🛑 ফায়ারওয়াল ১: জেমিনাই চেক
    print("\n[Step 1] Loading Story & Audio...")
    story_generated = generate_story()
    
    # যদি জেমিনাই ফেইল করে, প্রজেক্ট এখানেই বন্ধ হয়ে যাবে!
    if not story_generated:
        print("\n❌ CRITICAL ERROR: Gemini failed to generate a new story!")
        print("🛑 Pipeline Stopped: We will NOT upload a default/fake story to YouTube.")
        sys.exit(1) # স্ক্রিপ্ট বন্ধ

    # অডিও জেনারেট
    generate_audio(STORY_JSON_PATH)

    # 🛑 ফায়ারওয়াল ২: ইমেজ চেক
    print("\n[Step 2] Generating AI Images...")
    images_status = generate_images(STORY_JSON_PATH)
    
    if not images_status:
        print("\n❌ CRITICAL ERROR: Image generation failed (Leonardo/Flux Error)!")
        print("🛑 Pipeline Stopped: We will NOT upload a video without proper images.")
        sys.exit(1) # স্ক্রিপ্ট বন্ধ

    print("\n[Step 3 & 4] Rendering Animation Scenes & Shorts...")
    shorts_path = create_final_videos(STORY_JSON_PATH)

    if not shorts_path:
        print("\n❌ CRITICAL ERROR: Video rendering failed!")
        sys.exit(1)

    # ফায়ারওয়াল পার হলে তবেই আপলোড
    print("\n[Step 5] Headless YouTube Uploading...")
    upload_status = upload_to_youtube(shorts_path, STORY_JSON_PATH)
    
    if upload_status:
        print("\n🎉 Pipeline Execution Completed Successfully!")
    else:
        print("\n⚠️ Video created, but YouTube Upload Failed.")

if __name__ == "__main__":
    main()
