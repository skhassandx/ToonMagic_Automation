import os
import json
import random
import asyncio
import edge_tts
from google import genai
from config.settings import STORIES_DIR, AUDIO_DIR

# মাইক্রোসফটের রিয়েলিস্টিক বাংলা ভয়েস জেনারেটর ফাংশন
async def create_voice(text, file_path):
    # bn-BD-PradeepNeural হলো চমৎকার একটি বাংলাদেশী ভয়েস
    communicate = edge_tts.Communicate(text, "bn-BD-PradeepNeural")
    await communicate.save(file_path)

def generate_story_and_audio():
    story_path = os.path.join(STORIES_DIR, "latest_story.json")
    gemini_key = os.environ.get("GEMINI_API_KEY")
    story_data = None

    topics = [
        "এক বুদ্ধিমান শিয়াল ও জাদুর হীরা",
        "একটি উড়ন্ত লাল টুপি ও ছোট্ট রাজুর এডভেঞ্চার",
        "জাদুর টিয়া পাখি ও তার নতুন বন্ধু",
        "একটি হাসিখুশি রাক্ষস ও একটি জাদুর বাঁশি"
    ]

    if gemini_key:
        print("🧠 Generating unique daily story using Google Gemini AI...")
        try:
            client = genai.Client(api_key=gemini_key)
            
            prompt = """
            বাংলায় একটি দারুণ আকর্ষণীয় কার্টুন গল্পের স্ক্রিপ্ট তৈরি করো। 
            গল্পটি ৫ থেকে ৮ টি দৃশ্যের (scenes) মধ্যে যেকোনো একটি র্যান্ডম সংখ্যার হবে। 
            গল্পের বিষয়ের সাথে হুবহু মিল রেখে একটি ইউনিক টাইটেল এবং গল্প সংক্রান্ত ১০টি ট্যাগ তৈরি করবে।
            
            অবশ্যই নিচের বিশুদ্ধ JSON ফরম্যাটে রেসপন্স দাও (JSON ছাড়া অন্য কিছু লিখবে না):
            {
                "title": "গল্পের আকর্ষণীয় ইউনিক শিরোনাম",
                "tags": ["গল্পের ট্যাগ ১", "গল্পের ট্যাগ ২", "bangla cartoon", "kids story"],
                "scenes": [
                    {
                        "scene_number": 1,
                        "narration": "প্রথম দৃশ্যের বাংলা কাহিনী...",
                        "image_prompt": "Vertical 9:16 format, 3D Pixar style cartoon, cute 8-year-old boy in yellow t-shirt and blue shorts, standing in a magical forest, highly detailed"
                    }
                ]
            }
            [VERY IMPORTANT]: The 'image_prompt' MUST be in English. Decide a random number of scenes between 5 and 8. You MUST describe the EXACT same main character physically in EVERY single image_prompt so the character looks consistent.
            """
            
            response = client.models.generate_content(
                model='gemini-3.6-flash',
                contents=prompt
            )
            
            text = response.text.strip()
            if text.startswith("```json"):
                text = text[7:]
            if text.endswith("```"):
                text = text[:-3]
            text = text.strip()
            
            story_data = json.loads(text)
            print(f"✅ Unique Story Generated: {story_data.get('title')} ({len(story_data['scenes'])} scenes)")
        except Exception as e:
            print(f"⚠️ Gemini Story Gen Error: {e}")

    # ব্যাকআপ গল্প
    if not story_data or 'title' not in story_data:
        chosen_topic = random.choice(topics)
        scene_count = random.randint(5, 7)
        scenes = []
        for i in range(1, scene_count + 1):
            scenes.append({
                "scene_number": i, 
                "narration": f"{chosen_topic} নিয়ে গল্পের দৃশ্য নম্বর {i}।", 
                "image_prompt": f"Vertical 9:16 format, 3D Pixar style, magical scene about {chosen_topic}, cute character, bright colors"
            })
            
        story_data = {
            "title": chosen_topic,
            "tags": ["bangla cartoon", "bengali story", "kids golpo", "fairy tales", "moral story"],
            "scenes": scenes
        }

    with open(story_path, 'w', encoding='utf-8') as f:
        json.dump(story_data, f, ensure_ascii=False, indent=4)

    # নতুন ভয়েস ইঞ্জিন দিয়ে অডিও সেভ করা
    for scene in story_data['scenes']:
        scene_num = scene['scene_number']
        audio_path = os.path.join(AUDIO_DIR, f"scene_{scene_num}.mp3")
        
        if not os.path.exists(audio_path):
            print(f"🎙️ Generating Audio for Scene {scene_num}...")
            try:
                # Async ফাংশন রান করানো
                asyncio.run(create_voice(scene['narration'], audio_path))
            except Exception as e:
                print(f"⚠️ Audio Generation Error: {e}")

    return story_path
