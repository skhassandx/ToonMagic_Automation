import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BACKUP_DIR = os.path.join(BASE_DIR, 'backup')

STORIES_DIR = os.path.join(BACKUP_DIR, 'stories')
IMAGES_DIR = os.path.join(BACKUP_DIR, 'images')
AUDIO_DIR = os.path.join(BACKUP_DIR, 'audio')
ANIMATED_DIR = os.path.join(BACKUP_DIR, 'animated_scenes')
FINAL_DIR = os.path.join(BACKUP_DIR, 'final_videos')

# Ensure directories exist
for d in [STORIES_DIR, IMAGES_DIR, AUDIO_DIR, ANIMATED_DIR, FINAL_DIR]:
    os.makedirs(d, exist_ok=True)