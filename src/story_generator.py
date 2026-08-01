import os
import json
import random
from gtts import gTTS
import google.generativeai as genai
from config.settings import STORIES_DIR, AUDIO_DIR

def generate_story_and_audio():
    story_path = os.path.join(STORIES_DIR, "latest_story.json")
    
    # ১. প্রতিদিন নতুন ইউনিক গল্প তৈরির সিস্টেম (Gemini AI)
    gemini_key = os.environ.get("GEMINI_API_KEY")
    story_data = None

    if gemini_key:
        print("🧠 Generating unique daily story using Google Gemini AI...")
        try:
            genai.configure(api_key=gemini_key)
            model = genai.GenerativeModel('gemini-3.6-flash')
            
            prompt = """
            বাংলায় একটি দারুণ আকর্ষণীয় ও শিক্ষণীয় শিশুদের কার্টুন গল্পের স্ক্রিপ্ট তৈরি করো। 
            গল্পটিতে ঠিক ৪টি দৃশ্য (scene) থাকবে। 
            অবশ্যই নিচের মতো বিশুদ্ধ JSON ফরম্যাটে রেসপন্স দাও (অন্য কোনো অতিরিক্ত টেক্সট বা markdown দেবেনা):

            {
                "title": "গল্পের চমৎকার শিরোনাম",
                "scenes": [
                    {
                        "scene_number": 1,
                        "narration": "প্রথম দৃশ্যের বাংলা সুন্দর কাহিনী বা সংলাপ",
                        "image_prompt": "3D Pixar style cartoon scene, English prompt describing the scene for image generator"
                    },
                    {
                        "scene_number": 2,
                        "narration": "দ্বিতীয় দৃশ্যের বাংলা সুন্দর কাহিনী বা সংলাপ",
                        "image_prompt": "3D Pixar style cartoon scene, English prompt describing the scene for image generator"
                    },
                    {
                        "scene_number": 3,
                        "narration": "তৃতীয় দৃশ্যের বাংলা সুন্দর কাহিনী বা সংলাপ",
                        "image_prompt": "3D Pixar style cartoon scene, English prompt describing the scene for image generator"
                    },
                    {
                        "scene_number": 4,
                        "narration": "চতুর্থ দৃশ্যের বাংলা শিক্ষা ও সমাপ্তি",
                        "image_prompt": "3D Pixar style cartoon scene, English prompt describing the scene for image generator"
                    }
                ]
            }
            """
            response = model.generate_content(prompt)
            text = response.text.strip().replace("```json", "").replace("```", "").strip()
            story_data = json.loads(text)
            print(f"✅ Unique Story Generated: {story_data.get('title')}")
        except Exception as e:
            print(f"⚠️ Gemini Story Gen Error: {e}. Falling back to random story.")

    # যদি Gemini Key না থাকে, তবে বিভিন্ন দৈবচয়ন (Random) বাংলা গল্প তৈরি করবে
    if not story_data:
        random_id = random.randint(1000, 9999)
        topics = [
            ("বুদ্ধিমান খরগোশ ও বনের বন্ধুত্ব", "Cute intelligent Rabbit in magical forest"),
            ("মেহুল ও তার জাদুকরী রঙিন পেন্সিল", "Little Boy Mehul with Glowing Magical Pencil"),
            ("ছোট্ট টিয়া পাখি ও নদীর রাজহাঁস", "Cute Parrot and Swan in River Adventure"),
            ("বনের রাজপুত্র ও একটি জাদুকরী ফুল", "Little Prince in Magical Kingdom with Glowing Flower")
        ]
        chosen_title, chosen_prompt = random.choice(topics)
        story_data = {
            "title": f"{chosen_title} #{random_id}",
            "scenes": [
                {"scene_number": 1, "narration": f"আজকের গল্প {chosen_title}। সুন্দর এক সকালের ঘটনা।", "image_prompt": f"3D Pixar style cartoon scene, {chosen_prompt}, sunny morning"},
                {"scene_number": 2, "narration": "হঠাৎ তাদের সামনে একটি নতুন চমক বা সমস্যা দেখা দিল।", "image_prompt": f"3D Pixar style cartoon scene, {chosen_prompt}, mysterious surprise"},
                {"scene_number": 3, "narration": "সবাই বুদ্ধিমত্তা দিয়ে একসাথে সমস্যার সুন্দর সমাধান করল।", "image_prompt": f"3D Pixar style cartoon scene, {chosen_prompt}, solving problem happily"},
                {"scene_number": 4, "narration": "এখান থেকে আমরা শিখলাম ঐক্যবদ্ধ থাকলে সব বাধাই জয় করা যায়।", "image_prompt": f"3D Pixar style cartoon scene, {chosen_prompt}, happy ending with friends"}
            ]
        }

    with open(story_path, 'w', encoding='utf-8') as f:
        json.dump(story_data, f, ensure_ascii=False, indent=4)

    # ২. গল্পের অডিও তৈরি (gTTS)
    for scene in story_data['scenes']:
        scene_num = scene['scene_number']
        narration = scene['narration']
        audio_path = os.path.join(AUDIO_DIR, f"scene_{scene_num}.mp3")

        if not os.path.exists(audio_path):
            print(f"🔊 Audio generated for scene {scene_num}")
            tts = gTTS(text=narration, lang='bn')
            tts.save(audio_path)

    return story_path
