import os
import json
from gtts import gTTS
from config.settings import STORIES_DIR, AUDIO_DIR

DEFAULT_STORY = {
    "title": "টুটুল ও জাদুর পেন্সিল",
    "scenes": [
        {"scene_number": 1, "text": "আমাদের পাড়ার সবচেয়ে বড় ডানপিঠে ছেলে হলো টুটুল। সারাদিন শুধুই দুষ্টুমি।"},
        {"scene_number": 2, "text": "একদিন রাস্তায় হাঁটতে হাঁটতে হঠাৎ একটা চকচকে সোনালী পেন্সিল কুড়িয়ে পেল সে।"},
        {"scene_number": 3, "text": "টুটুল ভাবলো এতো দারুণ ব্যাপার! সে খাতায় একটা বিশাল বড় কুমির একে ফেললো।"},
        {"scene_number": 4, "text": "আঁকা শেষ হতেই খাতা থেকে একটা আস্ত কুমির সত্যি সত্যি লাফিয়ে ঘরের মেঝেতে চলে এলো।"},
        {"scene_number": 5, "text": "কুমিরটা খপ করে টুটুলের প্যান্টের পেছনে কামড় বসানোর জোগাড়! টুটুল তখন প্রানপণে দৌড় দিল।"},
        {"scene_number": 6, "text": "দৌড়াতে দৌড়াতে সে রবার দিয়ে কুমিরটাকে মুছে ফেলল এবং কসম খেল আর বদমাইশি করবে না।"}
    ]
}

def generate_story_and_audio():
    story_path = os.path.join(STORIES_DIR, "latest_story.json")
    
    if not os.path.exists(story_path):
        with open(story_path, 'w', encoding='utf-8') as f:
            json.dump(DEFAULT_STORY, f, ensure_ascii=False, indent=2)
        story_data = DEFAULT_STORY
    else:
        with open(story_path, 'r', encoding='utf-8') as f:
            story_data = json.load(f)

    # Generate Bangla Voiceover TTS for each scene
    for scene in story_data['scenes']:
        scene_num = scene['scene_number']
        audio_path = os.path.join(AUDIO_DIR, f"scene_{scene_num}.mp3")
        if not os.path.exists(audio_path):
            tts = gTTS(text=scene['text'], lang='bn')
            tts.save(audio_path)
            print(f"🔊 Audio generated for scene {scene_num}")

    return story_path