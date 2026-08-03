import os

# Base directory
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BACKUP_DIR = os.path.join(BASE_DIR, "backup")

# Sub-directories
STORIES_DIR = os.path.join(BACKUP_DIR, "stories")
IMAGES_DIR = os.path.join(BACKUP_DIR, "images")
AUDIO_DIR = os.path.join(BACKUP_DIR, "audio")
ANIMATED_DIR = os.path.join(BACKUP_DIR, "animated_scenes")
FINAL_VIDEOS_DIR = os.path.join(BACKUP_DIR, "final_videos")

# Create directories if they don't exist
for d in [STORIES_DIR, IMAGES_DIR, AUDIO_DIR, ANIMATED_DIR, FINAL_VIDEOS_DIR]:
    os.makedirs(d, exist_ok=True)

# 🌟 এই নতুন লাইনটি যোগ করা হলো
STORY_JSON_PATH = os.path.join(STORIES_DIR, "story.json")
