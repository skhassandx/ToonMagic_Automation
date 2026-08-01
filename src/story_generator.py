import os
import json
import random
from gtts import gTTS
from google import genai
from config.settings import STORIES_DIR, AUDIO_DIR

def generate_story_and_audio():
    story_path = os.path.join(STORIES_DIR, "latest_story.json")
    gemini_key = os.environ.get("GEMINI_API_KEY")
    story_data = None

    if gemini_key:
        print("🧠 Generating unique daily story using Google Gemini AI...")
        try:
            # লেটেস্ট Google GenAI ক্লায়েন্ট ব্যবহার করা হয়েছে (কোনো ওয়ার্নিং আসবে না)
            client = genai.Client(api_key=gemini_key)
            
            prompt = """
            বাংলায় একটি দারুণ আকর্ষণীয় শিশুদের কার্টুন গল্পের স্ক্রিপ্ট তৈরি করো। 
            গল্পটি ৫ থেকে ৮ টি দৃশ্যের (scenes) মধ্যে যেকোনো একটি র‍্যান্ডম সংখ্যার হবে (যেমন কখনো ৫টি, কখনো ৭টি বা ৮টি)। 
            অবশ্যই নিচের বিশুদ্ধ JSON ফরম্যাটে রেসপন্স দাও:
            {
                "title": "গল্পের চমৎকার নতুন শিরোনাম",
                "scenes": [
                    {
                        "scene_number": 1,
                        "narration": "প্রথম দৃশ্যের বাংলা কাহিনী...",
                        "image_prompt": "Vertical 9:16 format, 3D Pixar style, cute 8-year-old boy in yellow t-shirt and blue shorts, standing in a magical forest, highly detailed"
                    }
                ]
            }
            [VERY IMPORTANT]: The 'image_prompt' MUST be in English. Decide a random number of scenes between 5 and 8. You MUST describe the EXACT same main character physically in EVERY single image_prompt so the character looks consistent.
            """
            
            response = client.models.generate_content(
                model='gemini-1.5-flash',
                contents=prompt
            )
            
            text = response.text.strip().replace("```json", "").replace("```", "").strip()
            story_data = json.loads(text)
            print(f"✅ Unique Story Generated: {story_data.get('title')} ({len(story_data['scenes'])} scenes)")
        except Exception as e:
            print(f"⚠️ Gemini Story Gen Error: {e}")

    # ব্যাকআপ গল্প
    if not story_data:
        scene_count = random.randint(5, 8)
        scenes = []
        for i in range(1, scene_count + 1):
            scenes.append({
                "scene_number": i, 
                "narration": f"এটি গল্পের {i} নম্বর দৃশ্য।", 
                "image_prompt": "Vertical 9:16 format, 3D Pixar style, cute 8-year-old boy in yellow t-shirt"
            })
            
        story_data = {
            "title": f"মজার এক দিন #{random.randint(100,999)}",
            "scenes": scenes
        }

    with open(story_path, 'w', encoding='utf-8') as f:
        json.dump(story_data, f, ensure_ascii=False, indent=4)

    for scene in story_data['scenes']:
        scene_num = scene['scene_number']
        audio_path = os.path.join(AUDIO_DIR, f"scene_{scene_num}.mp3")
        if not os.path.exists(audio_path):
            tts = gTTS(text=scene['narration'], lang='bn')
            tts.save(audio_path)

    return story_path
