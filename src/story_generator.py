import os
import json
import random
import time
from google import genai
from google.genai import types
from config.settings import STORY_DIR

def generate_story():
    print("🧠 Generating Dynamic, Fast-Paced Story using Gemini (With Fallback)...")
    
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("❌ CRITICAL ERROR: GEMINI_API_KEY not found!")
        return False

    client = genai.Client(api_key=api_key)

    # 🌟 আপনার দেওয়া ৩০টি সম্পূর্ণ ভিন্ন ক্যাটাগরি
    genres = [
        "খুব হাসির এবং মজার কার্টুন গল্প", "অত্যন্ত ইমোশনাল এবং দুঃখের গল্প (Sad Story)",
        "শিক্ষামূলক এবং নীতিবাক্যমূলক গল্প (Educational)", "বাচ্চাদের মজার ছড়া বা কবিতা (Nursery Rhymes)",
        "খেলাধুলা এবং বন্ধুত্বের গল্প (Sports)", "ইসলামিক শিক্ষামূলক গল্প (Islamic Education)",
        "হাদিস থেকে নেওয়া ছোট্ট শিক্ষামূলক ঘটনা (Hadith Story)", "রূপকথার জাদুকরী গল্প (Fairy Tale)",
        "ভুতের বা রহস্যময় মজার গল্প (Funny Ghost Story)", "সাইন্স ফিকশন বা মহাকাশ ভ্রমণের গল্প (Sci-Fi/Space)",
        "চালাকপদে শিয়াল ও বোকা কুমিরের গল্প (Folk Tale)", "সুপারহিরো বাচ্চাদের সাহসিকতার গল্প (Superhero)",
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
    
    # 🌟 ম্যাজিক ট্রিক: সিন সংখ্যা ৬ থেকে ২০ এর মধ্যে র‍্যান্ডমলি সিলেক্ট হবে!
    scene_count = random.randint(6, 20) 
    
    # প্রতি সিন আনুমানিক ৩ সেকেন্ড ধরে মোট সময় ক্যালকুলেট করা হচ্ছে (Fast pacing)
    approx_duration = scene_count * 3 

    # 🌟 ডায়নামিক প্রম্পট (ছোট ও দ্রুত ন্যারেশন)
    prompt = f"""
    You are a professional YouTube Shorts scriptwriter. Write a short, engaging, and perfectly structured Bengali story script for an approximately {approx_duration}-second YouTube Shorts video. 

    Target Topic/Category: {selected_genre}

    The story must have a clear beginning, middle, and end. The narrative should flow smoothly and logically. Do NOT just write isolated dialogues or random phrases. Tell a complete story.

    The script must be divided into exactly {scene_count} scenes.

    For each scene, provide two things:
    1. "narration" (Bengali): A meaningful but VERY SHORT sentence telling the story. Keep it punchy and concise so it fits within 2-3 seconds per scene. Do not use long, complex sentences. Do not use isolated exclamations like "ওমা!", "হায় হায়!", write proper sentences.
    2. "image_prompt" (English): A highly detailed description for an AI image generator to create the scene. Describe the character, action, setting, lighting, and mood. Ensure it perfectly matches the narration. Include style tags like "3D Pixar style, highly detailed, colorful, wide landscape, full body character visible".

    Rules:
    - The story must be in Bengali.
    - Create a clear plot: Introduce a character, present a problem, show a magical or clever solution, and end with a moral or happy conclusion.
    - The output MUST be in valid JSON format only, following the exact structure below. Do not include markdown code blocks.

    JSON Format:
    {{
        "title": "গল্পের একটি আকর্ষণীয় বাংলা টাইটেল",
        "genre": "{selected_genre}",
        "scenes": [
            {{
                "scene_number": 1,
                "narration": "এক গ্রামে বাস করতো ছোট্ট সাহসী ছেলে রানা।",
                "image_prompt": "3D Pixar style, cute cartoon boy with black hair standing in a vibrant green village, smiling bravely, wide angle, highly detailed..."
            }}
        ]
    }}
    """

    # 🌟 আপনার আগের মতো মাল্টিপল মডেল ফলব্যাক সিস্টেম (৩.৬ কে প্রাইমারি হিসেবে রাখা হয়েছে)
    models_to_try = ['gemini-3.6-flash', 'gemini-3.6-flash', 'gemini-3.5-flash', 'gemini-3.0-flash']

    for attempt in range(3): 
        for model_name in models_to_try:
            try:
                print(f"🔄 Attempting with model: {model_name} | Scenes: {scene_count} | Duration: ~{approx_duration}s (Attempt {attempt+1})...")
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
