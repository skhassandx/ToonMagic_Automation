import os
import json
from config.settings import STORY_DIR
from src.story_generator import generate_story
from src.audio_generator import generate_audio
from src.image_generator import generate_images
from src.video_editor import create_video
from src.youtube_uploader import upload_to_youtube

def main():
    print("==========================================")
    print("🚀 ToonMagic Bangla - Automated Pipeline")
    print("==========================================")

    story_path = os.path.join(STORY_DIR, 'story.json')

    if not generate_story(): return
    if not generate_audio(story_path): return
    if not generate_images(story_path): return
    
    final_video_path = create_video(story_path)
    if not final_video_path: return
    
    # 🌟 জেনারেট হওয়া গল্পের ডেটা পড়া
    with open(story_path, 'r', encoding='utf-8') as f:
        story_data = json.load(f)
        video_title = story_data.get('title', 'Bangla Animated Short Story')
        video_genre = story_data.get('genre', 'Bangla Cartoon')
    
    description = f"Watch this amazing new story!\n\nCategory: {video_genre}\nCreated automatically by ToonMagic AI."

    # 🌟 আল্টিমেট প্লেলিস্ট ম্যাপিং (আপনার আসল আইডি যুক্ত করা হলো)
    playlist_map = {
        # ১. হাসির ও মজার কার্টুন
        "খুব হাসির এবং মজার কার্টুন গল্প": "PLTM7bJwT8Rv8",
        "বাচ্চাদের মজার ছড়া বা কবিতা (Nursery Rhymes)": "PLTM7bJwT8Rv8",
        "চালাক শিয়াল ও বোকা কুমিরের গল্প (Folk Tale)": "PLTM7bJwT8Rv8",
        "অলসতার পরিণতি নিয়ে মজার গল্প (Laziness)": "PLTM7bJwT8Rv8",
        "স্কুল জীবনের মজার স্মৃতি ও শিক্ষণীয় ঘটনা (School Life)": "PLTM7bJwT8Rv8",

        # ২. শিক্ষামূলক ও নীতিকথা
        "শিক্ষামূলক এবং নীতিবাক্যমূলক গল্প (Educational)": "PLZU3yfpAHzEM",
        "লোভের পরিণতি নিয়ে শিক্ষামূলক গল্প (Consequences of Greed)": "PLZU3yfpAHzEM",
        "সততা ও পুরস্কারের গল্প (Honesty & Reward)": "PLZU3yfpAHzEM",
        "অহংকার পতনের মূল- এই বিষয়ের উপর গল্প (Pride/Arrogance)": "PLZU3yfpAHzEM",
        "স্বাস্থ্য, পরিচ্ছন্নতা ও ভালো অভ্যাসের গল্প (Good Habits)": "PLZU3yfpAHzEM",
        "দানশীলতা ও অপরকে সাহায্য করার গল্প (Charity/Helping)": "PLZU3yfpAHzEM",
        "পরিবেশ বাঁচানো ও গাছ লাগানোর সচেতনতামূলক গল্প (Environment)": "PLZU3yfpAHzEM",
        "গ্রামের সাধারণ জীবন ও মা-বাবার ভালোবাসার গল্প (Village Life)": "PLZU3yfpAHzEM",
        "অত্যন্ত ইমোশনাল এবং দুঃখের গল্প (Sad Story)": "PLZU3yfpAHzEM",

        # ৩. রূপকথা ও জাদুকরী গল্প
        "রূপকথার জাদুকরী গল্প (Fairy Tale)": "PLccn5jUqTKAK",
        "জাদুকরী গাছ ও প্রাণীদের কথা বলার গল্প (Talking Animals)": "PLccn5jUqTKAK",
        "রাজা, রানী ও রাজকন্যার অ্যাডভেঞ্চার গল্প (Royal Adventure)": "PLccn5jUqTKAK",
        "জাদুর পেন্সিল বা জাদুর প্রদীপের মজার ঘটনা (Magic Item)": "PLccn5jUqTKAK",
        "সমুদ্রের নিচের জগৎ ও জলপরীদের গল্প (Mermaids/Underwater)": "PLccn5jUqTKAK",

        # ৪. ইসলামিক শিক্ষামূলক গল্প
        "ইসলামিক শিক্ষামূলক গল্প (Islamic Education)": "PLJQRqlqH37EY",
        "হাদিস থেকে নেওয়া ছোট্ট শিক্ষামূলক ঘটনা (Hadith Story)": "PLJQRqlqH37EY",
        "নবী-রাসূলদের জীবনের শিক্ষামূলক ছোট ঘটনা (Prophets' Stories)": "PLJQRqlqH37EY",

        # ৫. পশুপাখিদের মজার গল্প
        "বুদ্ধিমান কাক বা পাখির বুদ্ধিদীপ্ত গল্প (Clever Birds)": "PLRYQPRJmPGkM",
        "কৃষক ও তার পোষা প্রাণীর বন্ধুত্বের গল্প (Farmer & Pets)": "PLRYQPRJmPGkM",

        # ৬. অ্যাডভেঞ্চার ও সাই-ফাই
        "সুপারহিরো বাচ্চাদের সাহসিকতার গল্প (Superhero)": "PLAUlcFlAF_Jo",
        "সাইন্স ফিকশন বা মহাকাশ ভ্রমণের গল্প (Sci-Fi/Space)": "PLAUlcFlAF_Jo",
        "টাইম ট্রাভেল বা সময় ভ্রমণের মজার গল্প (Time Travel)": "PLAUlcFlAF_Jo",
        "ভবিষ্যতের আধুনিক দুনিয়া নিয়ে মজার গল্প (Future World)": "PLAUlcFlAF_Jo",
        "খেলাধুলা এবং বন্ধুত্বের গল্প (Sports)": "PLAUlcFlAF_Jo",

        # ৭. ভুতের ও রহস্যের গল্প
        "ভুতের বা রহস্যময় মজার গল্প (Funny Ghost Story)": "PLOSv98OMol24"
    }

    # বর্তমান গল্পের ক্যাটাগরি অনুযায়ী অটোমেটিক প্লেলিস্ট আইডি সিলেক্ট করবে
    target_playlist_id = playlist_map.get(video_genre, None)
    
    # 🌟 ইউটিউব আপলোড (প্লেলিস্ট আইডি সহ)
    try:
        upload_to_youtube(final_video_path, video_title, description, playlist_id=target_playlist_id)
        print("🎉 PIPELINE COMPLETED SUCCESSFULLY!")
    except Exception as e:
        print(f"⚠️ Video rendered but upload failed: {e}")

if __name__ == "__main__":
    main()
