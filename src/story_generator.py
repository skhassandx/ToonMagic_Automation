import os
import json
import random
from gtts import gTTS
import google.generativeai as genai
from config.settings import STORIES_DIR, AUDIO_DIR

def generate_story_and_audio():
    story_path = os.path.join(STORIES_DIR, "latest_story.json")
    gemini_key = os.environ.get("GEMINI_API_KEY")
    story_data = None

    if gemini_key:
        print("🧠 Generating unique daily story using Google Gemini AI...")
        try:
            genai.configure(api_key=gemini_key)
            # একদম স্ট্যাবল এবং কাজ করে এমন মডেল
            model = genai.GenerativeModel('gemini-3.6-flash')
            
            prompt = """
            বাংলায় একটি দারুণ আকর্ষণীয় শিশুদের কার্টুন গল্পের স্ক্রিপ্ট তৈরি করো। 
            ঠিক ৮টি দৃশ্য (scene) থাকবে। 
            অবশ্যই নিচের বিশুদ্ধ JSON ফরম্যাটে রেসপন্স দাও:
            {
                "title": "গল্পের চমৎকার নতুন শিরোনাম",
                "scenes": [
                    {
                        "scene_number": 1,
                        "narration": "প্রথম দৃশ্যের বাংলা কাহিনী...",
                        "image_prompt": "Vertical 9:16 format, 3D Pixar style, cute 8-year-old boy in red shirt and blue jeans, black hair, standing in a beautiful village, highly detailed"
                    }
                ]
            }
            [VERY IMPORTANT]: The 'image_prompt' MUST be in English. You MUST describe the EXACT same main character (e.g., boy in red shirt and blue jeans) physically in EVERY single image_prompt so the character looks consistent. Ensure exactly 8 scenes are generated.
            """
            response = model.generate_content(prompt)
            text = response.text.strip().replace("```json", "").replace("```", "").strip()
            story_data = json.loads(text)
            print(f"✅ Unique Story Generated: {story_data.get('title')}")
        except Exception as e:
            print(f"⚠️ Gemini Story Gen Error: {e}")

    # ব্যাকআপ গল্প
    if not story_data:
        story_data = {
            "title": f"মজার এক দিন #{random.randint(100,999)}",
            "scenes": [
                {"scene_number": 1, "narration": "এক গ্রামে ছিল এক বুদ্ধিমান ছেলে।", "image_prompt": "Vertical 9:16 format, 3D Pixar style, cute 8-year-old boy in red shirt and blue jeans"}
            ]
        }
        with open(story_path, 'w', encoding='utf-8') as f:
            json.dump(story_data, f, ensure_ascii=False, indent=4)
        return story_path

    with open(story_path, 'w', encoding='utf-8') as f:
        json.dump(story_data, f, ensure_ascii=False, indent=4)

    for scene in story_data['scenes']:
        scene_num = scene['scene_number']
        audio_path = os.path.join(AUDIO_DIR, f"scene_{scene_num}.mp3")
        if not os.path.exists(audio_path):
            tts = gTTS(text=scene['narration'], lang='bn')
            tts.save(audio_path)

    return story_path
