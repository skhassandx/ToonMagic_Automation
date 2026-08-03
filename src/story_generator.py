import os
import json
import random
# 🌟 পুরোনো google.generativeai বাদ দিয়ে নতুন google.genai ইমপোর্ট করা হলো
from google import genai
from config.settings import STORY_JSON_PATH

def generate_story():
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("❌ CRITICAL ERROR: GEMINI_API_KEY not found in environment variables!")
        return False

    # 🌟 নতুন SDK এর ক্লায়েন্ট সেটআপ
    try:
        client = genai.Client(api_key=api_key)
    except Exception as e:
        print(f"❌ Failed to initialize new Gemini Client: {e}")
        return False
    
    themes = [
        "a funny adventure of a clever fox and a lazy bear",
        "an emotional story about a little boy finding a lost puppy",
        "an educational story about a talking tree teaching the importance of water",
        "a magical rhyming story about a flying carpet and a brave girl",
        "a mysterious story about a glowing cave and a curious rabbit",
        "a moral story about two friends learning the value of honesty"
    ]
    selected_theme = random.choice(themes)
    
    prompt = f"""
    Write a short, engaging YouTube Shorts cartoon story in Bengali about {selected_theme}.
    The story must have exactly 5 scenes.
    
    IMPORTANT: You must return ONLY a valid, parseable JSON object. 
    Do not add any markdown formatting like ```json or ``` at the beginning or end.
    
    The JSON must follow this exact structure:
    {{
      "title": "Story Title Here",
      "scenes": [
        {{
          "scene_number": 1,
          "narration": "Bengali narration for scene 1",
          "image_prompt": "English prompt for image generation, highly detailed, 3D Pixar style"
        }}
      ]
    }}
    """
    
    try:
        print(f"🧠 Asking Gemini (New SDK) to write a {selected_theme} story...")
        
        # 🌟 নতুন SDK এর জেনারেট কন্টেন্ট কল এবং gemini-1.5-flash ব্যবহার
        response = client.models.generate_content(
            model='gemini-3.6-flash',
            contents=prompt
        )
        
        response_text = response.text.strip()
        if response_text.startswith("```json"):
            response_text = response_text[7:]
        if response_text.endswith("```"):
            response_text = response_text[:-3]
        response_text = response_text.strip()
            
        story_data = json.loads(response_text)
        
        with open(STORY_JSON_PATH, 'w', encoding='utf-8') as f:
            json.
