import os
from src.story_generator import generate_story_and_audio
from src.video_generator import animate_scenes
from src.video_editor import create_final_videos
from src.youtube_uploader import upload_to_youtube_headless

def main():
    print("==================================================")
    print("🚀 ToonMagic Bangla - Automated Pipeline Starting")
    print("==================================================")

    # 1. Generate / Load Story & Audio
    print("\n[Step 1] Loading Story & Audio...")
    story_path = generate_story_and_audio()

    # 2. Render Animation Scenes
    print("\n[Step 2] Rendering Animation Scenes via Replicate...")
    animate_scenes(story_path)

    # 3. Edit & Create Videos (Full + Shorts)
    print("\n[Step 3] Editing Video & Converting to 9:16 Shorts...")
    full_path, shorts_path = create_final_videos(story_path)

    # 4. Upload Shorts to YouTube
    if shorts_path and os.path.exists(shorts_path):
        print("\n[Step 4] Headless YouTube Uploading...")
        upload_to_youtube_headless(shorts_path)

    print("\n🎉 Pipeline Execution Completed Successfully!")

if __name__ == '__main__':
    main()
