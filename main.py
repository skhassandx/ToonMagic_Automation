import os
import json
from config.settings import STORY_DIR
from src.story_generator import generate_story
from src.audio_generator import generate_audio
from src.image_generator import generate_images
from src.video_editor import create_video
from src.youtube_uploader import upload_to_youtube

def main():
    print("==========================================")
    print("🚀 ToonMagic Bangla - Automated Pipeline")
    print("==========================================")

    # Step 1: Story Generation
    if not generate_story():
        print("❌ Pipeline failed at Story Generation step.")
        return

    story_path = os.path.join(STORY_DIR, 'story.json')

    # Step 2: Audio Generation
    if not generate_audio(story_path):
        print("❌ Pipeline failed at Audio Generation step.")
        return

    # Step 3: Image Generation
    if not generate_images(story_path):
        print("❌ Pipeline failed at Image Generation step.")
        return

    # Step 4: Video Editing
    video_path = create_video(story_path)
    if not video_path:
        print("❌ Pipeline failed at Video Editing step.")
        return

    # Step 5: YouTube Upload
    with open(story_path, 'r', encoding='utf-8') as f:
        story_data = json.load(f)

    title = story_data.get('title', 'মজার বাংলা কার্টুন গল্প')
    description = f"গল্পের ক্যাটাগরি: {story_data.get('genre', 'কার্টুন')}"

    try:
        upload_to_youtube(video_path, title, description)
        print("🎉 PIPELINE COMPLETED SUCCESSFULLY!")
    except Exception as e:
        print(f"⚠️ Video rendered but upload failed: {e}")

if __name__ == "__main__":
    main()
