import os
import json
import asyncio
import edge_tts
from config.settings import AUDIO_DIR

async def generate_audio_async(story_path):
    with open(story_path, 'r', encoding='utf-8') as f:
        story_data = json.load(f)
        
    for scene in story_data['scenes']:
        scene_num = scene['scene_number']
        aud_path = os.path.join(AUDIO_DIR, f"scene_{scene_num}.mp3")
        text = scene.get('narration', '')
        
        if text and not os.path.exists(aud_path):
            print(f"🎙️ Generating Audio for Scene {scene_num}...")
            # প্রফেশনাল বাংলা ভয়েস
            communicate = edge_tts.Communicate(text, "bn-BD-PradeepNeural")
            await communicate.save(aud_path)
            print(f"✅ Scene {scene_num} audio saved!")

def generate_audio(story_path):
    asyncio.run(generate_audio_async(story_path))
