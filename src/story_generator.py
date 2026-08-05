import os
import json
import random
from google import genai
from google.genai import types
from config.settings import STORY_DIR

def generate_story():
    print("🧠 Generating Dynamic & Unique Story using Gemini...")
    
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("❌ CRITICAL ERROR: GEMINI_API_KEY not found!")
        return False

    client = genai.Client(api_key=api_key)

    # 🌟 ১. মাল্টিপল গল্পের ধরন (এখানে আরও যোগ করতে পারবেন)
    genres = [
        "খুব হাসির এবং মজার কার্টুন গল্প",
        "অত্যন্ত ইমোশনাল এবং দুঃখের গল্প (Sad Story)",
        "শিক্ষামূলক এবং নীতিবাক্যমূলক গল্প (Educational)",
        "বাচ্চাদের মজার ছড়া বা কবিতা (Nursery Rhymes)",
        "খেলাধুলা এবং বন্ধুত্বের গল্প (Sports)",
        "ইসলামিক শিক্ষামূলক গল্প (Islamic Education)",
        "হাদিস থেকে নেওয়া ছোট্ট শিক্ষামূলক ঘটনা (Hadith Story)",
        "রূপকথার জাদুকরী গল্প (Fairy Tale)",
        "ভুতের বা রহস্যময় মজার গল্প (Funny Ghost Story)"
    ]
    
    # স্বয়ংক্রিয়ভাবে একটি ধরন বেছে নেওয়া
    selected_genre = random.choice(genres)
    
    # 🌟 ২. সিনের সংখ্যা ডাইনামিক করা (৭ থেকে ১২টি সিন)
    scene_count = random.randint(7, 12) 
    
    # 🌟 ৩. ভিডিওর সময়সীমা ডাইনামিক করা (৪০ থেকে ৫৮ সেকেন্ড)
    target_duration = random.randint(40, 58)

    prompt = f"""
    তুমি একজন প্রফেশনাল ইউটিউব শর্টস স্ক্রিপ্ট রাইটার। তোমাকে সম্পূর্ণ নতুন, ইউনিক এবং আকর্ষনীয় একটি বাংলা গল্প লিখতে হবে।
    আগের কোনো গল্পের সাথে এর বিন্দুমাত্র মিল থাকা যাবে না। সম্পূর্ণ নতুন ক্যারেক্টার এবং নতুন প্লট ব্যবহার করবে।

    আজকের গল্পের ধরন: {selected_genre}

    নির্দেশনা:
    ১. গল্পটি এমনভাবে লিখবে যেন ভয়েসওভার পড়লে মোট সময় ঠিক {target_duration} সেকেন্ডের কাছাকাছি হয়।
    ২. ভিডিওটি ফাস্ট-পেসড (Fast-paced) শর্টস হবে, তাই মোট {scene_count} টি ছোট ছোট সিন (Scene) তৈরি করবে।
    ৩. প্রতিটি সিনের 'narration' হবে একদম ছোট (১টি ছোট বাক্য), যাতে সিনগুলো খুব দ্রুত পরিবর্তন হয় এবং দর্শক বোর না হয়।
    ৪. image_prompt-এ "3D Pixar animation style, highly detailed, full body, wide angle" কথাগুলো যুক্ত করে দিবে এবং ওই সিনের সাথে মিল রেখে ক্যারেক্টার ও ব্যাকগ্রাউন্ডের বর্ণনা দেবে।
    ৫. আউটপুট অবশ্যই নিচের JSON ফরম্যাটে দেবে, এর বাইরে কোনো টেক্সট বা মার্কডাউন (যেমন ```json) লিখবে না।

    JSON Format:
    {{
        "title": "গল্পের একটি আকর্ষণীয় এবং এসইও অপটিমাইজড বাংলা টাইটেল",
        "genre": "{selected_genre}",
        "scenes": [
            {{
                "scene_number": 1,
                "narration": "বাংলায় ছোট্ট ভয়েসওভার...",
                "image_prompt": "3D Pixar style, cute boy walking in a village, wide angle, highly detailed..."
            }},
            ... (এভাবে ঠিক {scene_count} টি সিন)
        ]
    }}
    """

    for attempt in range(3):
        try:
            # 🌟 Temperature 0.9 দেওয়া হলো যাতে প্রতিদিন একদম ১০০% নতুন আইডিয়া জেনারেট হয়
            response = client.models.generate_content(
                model='gemini-3.5-flash', 
                contents=prompt,
                config=types.GenerateContentConfig(
                    response_mime_type="application/json",
                    temperature=0.9 
                )
            )

            story_text = response.text
            
            # JSON ক্লিনিং
            if story_text.startswith("```json"):
                story_text = story_text.replace("```json", "").replace("```", "").strip()
            elif story_text.startswith("```"):
                story_text = story_text.replace("```", "").strip()
                
            story_data = json.loads(story_text)

            os.makedirs(STORY_DIR, exist_ok=True)
            story_path = os.path.join(STORY_DIR, 'story.json')
            
            with open(story_path, 'w', encoding='utf-8') as f:
                json.dump(story_data, f, ensure_ascii=False, indent=4)

            print(f"✅ Unique Story Generated! Genre: {selected_genre} | Scenes: {scene_count} | Target Time: {target_duration}s")
            return True

        except Exception as e:
            print(f"⚠️ Attempt {attempt+1} Failed: {e}")
            time.sleep(5)

    print("❌ Failed to generate story after 3 attempts.")
    return False
