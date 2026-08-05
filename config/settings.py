import os

# প্রজেক্টের মেইন ডিরেক্টরি
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# ডেটা এবং স্টোরি ফোল্ডার
DATA_DIR = os.path.join(BASE_DIR, 'data')
STORY_DIR = os.path.join(DATA_DIR, 'story')  # 🌟 এই লাইনটিই মিসিং ছিল

# আউটপুট ফোল্ডার (অডিও, ইমেজ, ভিডিও)
OUTPUT_DIR = os.path.join(BASE_DIR, 'output')
AUDIO_DIR = os.path.join(OUTPUT_DIR, 'audio')
IMAGES_DIR = os.path.join(OUTPUT_DIR, 'images')

# ফোল্ডারগুলো আগে থেকে না থাকলে স্বয়ংক্রিয়ভাবে তৈরি করে নেবে
os.makedirs(STORY_DIR, exist_ok=True)
os.makedirs(AUDIO_DIR, exist_ok=True)
os.makedirs(IMAGES_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)
