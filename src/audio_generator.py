import os
import json
from gtts import gTTS
from config.settings import AUDIO_DIR

def generate_audio(story_path):
    print("🎙️ Generating Voiceover Audio...")
    with open(story_path, 'r', encoding='utf-8') as f:
        story_data = json.load(f)

    for scene in story_data['scenes']:
        scene_num = scene['scene_number']
        narration = scene['narration']
        audio_path = os.path.join(AUDIO_DIR, f"scene_{scene_num}.mp3")

        if os.path.exists(audio_path):
            continue

        try:
            tts = gTTS(text=narration, lang='bn', slow=False)
            tts.save(audio_path)
            print(f"✅ Scene {scene_num} audio saved!")
        except Exception as e:
            print(f"❌ Audio error in Scene {scene_num}: {e}")
            return False

    return True
