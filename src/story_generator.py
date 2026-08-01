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
            model = genai.GenerativeModel('gemini-2.5-flash')
            
            prompt = """
            বাংলায় একটি দারুণ আকর্ষণীয় শিশুদের কার্টুন গল্পের স্ক্রিপ্ট তৈরি করো। 
            গল্পটি একটু বড় হবে, তাই ঠিক ৮টি দৃশ্য (scene) থাকবে। 
            প্রতিটি দৃশ্যের ন্যারেশন (narration) অন্তত ২-৩ লাইনের হবে, যাতে ভিডিওটি প্রায় ৫৫-৬০ সেকেন্ডের কাছাকাছি হয়।
            অবশ্যই নিচের বিশুদ্ধ JSON ফরম্যাটে রেসপন্স দাও (অন্য কোনো টেক্সট দেবে না):
            {
                "title": "গল্পের শিরোনাম",
                "scenes": [
                    {
                        "scene_number": 1,
                        "narration": "প্রথম দৃশ্যের বাংলা কাহিনী...",
                        "image_prompt": "3D Pixar style, cute 8-year-old boy in red shirt standing in a beautiful village, highly detailed"
                    }
                ]
            }
            [VERY IMPORTANT]: The 'image_prompt' MUST be in English. You MUST describe the main character physically in EVERY single image_prompt so the scene is never empty. Ensure exactly 8 scenes are generated.
            """
            response = model.generate_content(prompt)
            text = response.text.strip().replace("```json", "").replace("```", "").strip()
            story_data = json.loads(text)
            print(f"✅ Unique Story Generated: {story_data.get('title')} with {len(story_data['scenes'])} scenes.")
        except Exception as e:
            print(f"⚠️ Gemini Story Gen Error: {e}")

    # ব্যাকআপ গল্প (যদি API ফেইল করে)
    if not story_data:
        story_data = {
            "title": f"টুটুল ও জাদুর বন #{random.randint(10,99)}",
            "scenes": [
                {"scene_number": 1, "narration": "এক গ্রামে ছিল টুটুল নামের এক ছোট্ট ছেলে। তার খুব শখ ছিল নতুন কিছু খোঁজার।", "image_prompt": "3D Pixar style, cute 8-year-old boy in red shirt standing in a sunny village"},
                {"scene_number": 2, "narration": "একদিন সে গ্রামের পেছনের এক অদ্ভুত জঙ্গলে গিয়ে হাজির হলো।", "image_prompt": "3D Pixar style, cute boy in red shirt entering a magical glowing forest"},
                {"scene_number": 3, "narration": "সেখানে সে পেলো এক জাদুর পেন্সিল, যা থেকে আলো বেরোচ্ছিল।", "image_prompt": "3D Pixar style, cute boy looking amazed at a glowing magical pencil in his hand"},
                {"scene_number": 4, "narration": "পেন্সিল দিয়ে মাটিতে সে একটি পাখির ছবি আঁকলো।", "image_prompt": "3D Pixar style, cute boy drawing a beautiful bird on the ground"},
                {"scene_number": 5, "narration": "অবাক কান্ড! পাখিটি সত্যি সত্যি জীবন্ত হয়ে আকাশে উড়ে গেল।", "image_prompt": "3D Pixar style, glowing magical bird flying away from the cute boy"},
                {"scene_number": 6, "narration": "এরপর সে আঁকলো একটি বিশাল সুন্দর ফুল।", "image_prompt": "3D Pixar style, cute boy looking at a giant glowing magical flower"},
                {"scene_number": 7, "narration": "ফুলের গন্ধে বনের সব পাখিরা তার কাছে ছুটে এলো।", "image_prompt": "3D Pixar style, many cute birds surrounding the happy boy with red shirt"},
                {"scene_number": 8, "narration": "টুটুল বুঝতে পারলো, জাদুর পেন্সিল দিয়ে সে সবার মুখে হাসি ফোটাতে পারবে।", "image_prompt": "3D Pixar style, cute boy laughing happily with magical creatures around him"}
            ]
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
