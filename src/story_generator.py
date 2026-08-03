import os
import json
import random
import google.generativeai as genai
from config.settings import STORY_JSON_PATH

def generate_story():
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("❌ CRITICAL ERROR: GEMINI_API_KEY not found in environment variables!")
        return False

    genai.configure(api_key=api_key)
    
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
        print(f"🧠 Asking Gemini to write a {selected_theme} story...")
        # 🌟 মডেল পরিবর্তন করে সবচেয়ে স্টেবল gemini-pro দেওয়া হলো
        model = genai.GenerativeModel('gemini-pro')
        response = model.generate_content(prompt)
        
        response_text = response.text.strip()
        if response_text.startswith("```json"):
            response_text = response_text[7:]
        if response_text.endswith("```"):
            response_text = response_text[:-3]
        response_text = response_text.strip()
            
        story_data = json.loads(response_text)
        
        with open(STORY_JSON_PATH, 'w', encoding='utf-8') as f:
            json.dump(story_data, f, ensure_ascii=False, indent=4)
            
        print(f"✅ Unique Story Generated Successfully: {story_data['title']} ({len(story_data['scenes'])} scenes)")
        return True
        
    except json.JSONDecodeError as e:
        print(f"⚠️ Gemini JSON Error: {e}. Gemini returned invalid format.")
        return False
    except Exception as e:
        print(f"⚠️ Gemini Generation Error: {e}")
        return False

if __name__ == "__main__":
    generate_story()
