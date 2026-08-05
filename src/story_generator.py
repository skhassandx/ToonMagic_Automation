import os
import json
import random
import time
from google import genai
from google.genai import types
from config.settings import STORY_DIR

def generate_story():
    print("🧠 Generating Dynamic, Emotional & Unique Story using Gemini (With Fallback)...")
    
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("❌ CRITICAL ERROR: GEMINI_API_KEY not found!")
        return False

    client = genai.Client(api_key=api_key)

    # 🌟 ৩০টি সম্পূর্ণ ভিন্ন ক্যাটাগরি
    genres = [
        "খুব হাসির এবং মজার কার্টুন গল্প", "অত্যন্ত ইমোশনাল এবং দুঃখের গল্প (Sad Story)",
        "শিক্ষামূলক এবং নীতিবাক্যমূলক গল্প (Educational)", "বাচ্চাদের মজার ছড়া বা কবিতা (Nursery Rhymes)",
        "খেলাধুলা এবং বন্ধুত্বের গল্প (Sports)", "ইসলামিক শিক্ষামূলক গল্প (Islamic Education)",
        "হাদিস থেকে নেওয়া ছোট্ট শিক্ষামূলক ঘটনা (Hadith Story)", "রূপকথার জাদুকরী গল্প (Fairy Tale)",
        "ভুতের বা রহস্যময় মজার গল্প (Funny Ghost Story)", "সাইন্স ফিকশন বা মহাকাশ ভ্রমণের গল্প (Sci-Fi/Space)",
        "চালাক শিয়াল ও বোকা কুমিরের গল্প (Folk Tale)", "সুপারহিরো বাচ্চাদের সাহসিকতার গল্প (Superhero)",
        "জাদুকরী গাছ ও প্রাণীদের কথা বলার গল্প (Talking Animals)", "গ্রামের সাধারণ জীবন ও মা-বাবার ভালোবাসার গল্প (Village Life)",
        "লোভের পরিণতি নিয়ে শিক্ষামূলক গল্প (Consequences of Greed)", "সততা ও পুরস্কারের গল্প (Honesty & Reward)",
        "স্বাস্থ্য, পরিচ্ছন্নতা ও ভালো অভ্যাসের গল্প (Good Habits)", "টাইম ট্রাভেল বা সময় ভ্রমণের মজার গল্প (Time Travel)",
        "সমুদ্রের নিচের জগৎ ও জলপরীদের গল্প (Mermaids/Underwater)", "বুদ্ধিমান কাক বা পাখির বুদ্ধিদীপ্ত গল্প (Clever Birds)",
        "রাজা, রানী ও রাজকন্যার অ্যাডভেঞ্চার গল্প (Royal Adventure)", "নবী-রাসূলদের জীবনের শিক্ষামূলক ছোট ঘটনা (Prophets' Stories)",
        "অহংকার পতনের মূল- এই বিষয়ের উপর গল্প (Pride/Arrogance)", "পরিবেশ বাঁচানো ও গাছ লাগানোর সচেতনতামূলক গল্প (Environment)",
        "জাদুর পেন্সিল বা জাদুর প্রদীপের মজার ঘটনা (Magic Item)", "স্কুল জীবনের মজার স্মৃতি ও শিক্ষণীয় ঘটনা (School Life)",
        "অলসতার পরিণতি নিয়ে মজার গল্প (Laziness)", "দানশীলতা ও অপরকে সাহায্য করার গল্প (Charity/Helping)",
        "কৃষক ও তার পোষা প্রাণীর বন্ধুত্বের গল্প (Farmer & Pets)", "ভবিষ্যতের আধুনিক দুনিয়া নিয়ে মজার গল্প (Future World)"
    ]
    
    selected_genre = random.choice(genres)
    scene_count = random.randint(12, 18) 
    target_duration = random.randint(40, 58) 

    prompt = f"""
    তুমি একজন প্রফেশনাল ইউটিউব শর্টস স্ক্রিপ্ট রাইটার। তোমাকে সম্পূর্ণ নতুন, ইউনিক এবং আকর্ষনীয় একটি বাংলা গল্প লিখতে হবে।
    আগের কোনো গল্পের সাথে এর বিন্দুমাত্র মিল থাকা যাবে না। সম্পূর্ণ নতুন ক্যারেক্টার এবং নতুন প্লট ব্যবহার করবে।

    আজকের গল্পের ধরন: {selected_genre}

    নির্দেশনা:
    ১. গল্পটি এমনভাবে লিখবে যেন ভয়েসওভার পড়লে মোট সময় ঠিক {target_duration} সেকেন্ডের কাছাকাছি হয়।
    ২. ভিডিওটি ফাস্ট-পেসড (Fast-paced) অ্যানিমেশন শর্টস হবে, তাই মোট {scene_count} টি ছোট ছোট সিন (Scene) তৈরি করবে।
    ৩. 🌟 আবেগ ও ভয়েসওভার টোন: প্রতিটি সিনের 'narration'-এ আবেগপূর্ণ শব্দ বা বিস্ময়সূচক অব্যয় (যেমন: ওমা!, হায় হায়!, হাহাহা!, ওরে বাবা!, ইশ!) ব্যবহার করবে, যাতে রোবটিক ভয়েসওভারটিও মানুষের মতো জীবন্ত ও এক্সপ্রেসিভ শোনায়। গল্পের ধরন অনুযায়ী টোন (খুশি, দুঃখ, ভয়, চমক) ফুটিয়ে তুলবে।
    ৪. 🌟 ছবির এক্সপ্রেশন: প্রতিটি 'image_prompt'-এ ক্যারেক্টারের চেহারার স্পষ্ট এক্সপ্রেশন (যেমন: crying bitterly, laughing out loud, looking extremely surprised, angry face) অবশ্যই উল্লেখ করবে। সাথে "3D Pixar style, highly detailed, colorful, wide landscape, full body character visible" ফরম্যাট ব্যবহার করবে।
    ৫. আউটপুট অবশ্যই শুদ্ধ JSON ফরম্যাটে দেবে।

    JSON Format:
    {{
        "title": "গল্পের একটি আকর্ষণীয় বাংলা টাইটেল",
        "genre": "{selected_genre}",
        "scenes": [
            {{
                "scene_number": 1,
                "narration": "ওমা! দেখো দেখো কী সুন্দর পাখি...",
                "image_prompt": "3D Pixar style, cute boy looking very surprised and happy pointing at a bird, wide angle, full body visible..."
            }}
        ]
    }}
    """

    # 🌟 সেরা কোয়ালিটি (Pro) থেকে শুরু করে স্ট্যাবল স্পিড (Flash) পর্যন্ত ফলব্যাক লজিক
    models_to_try = ['gemini-3.1-pro-preview', 'gemini-3.6-flash', 'gemini-3.5-flash']

    for attempt in range(3): 
        for model_name in models_to_try:
            try:
                print(f"🔄 Attempting with model: {model_name} (Attempt {attempt+1})...")
                response = client.models.generate_content(
                    model=model_name,
                    contents=prompt,
                    config=types.GenerateContentConfig(
                        response_mime_type="application/json",
                        temperature=0.95
                    )
                )

                story_text = response.text.strip()
                if story_text.startswith("```json"):
                    story_text = story_text.replace("```json", "").replace("```", "").strip()
                elif story_text.startswith("```"):
                    story_text = story_text.replace("```", "").strip()

                story_data = json.loads(story_text)

                story_path = os.path.join(STORY_DIR, 'story.json')
                with open(story_path, 'w', encoding='utf-8') as f:
                    json.dump(story_data, f, ensure_ascii=False, indent=4)

                print(f"✅ Success! Generated with {model_name} | Genre: {selected_genre} | Scenes: {scene_count}")
                return True

            except Exception as e:
                print(f"⚠️ {model_name} failed: {e}")
                print("⏳ Waiting 5 seconds before trying the next model...")
                time.sleep(5) 

    print("❌ Failed to generate story after all retries and model fallbacks.")
    return False
