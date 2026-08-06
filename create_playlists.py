import os
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials

def create_youtube_playlists():
    print("🚀 Creating SEO Optimized Playlists for ToonMagic Bangla...")

    client_id = os.environ.get("YOUTUBE_CLIENT_ID")
    client_secret = os.environ.get("YOUTUBE_CLIENT_SECRET")
    refresh_token = os.environ.get("YOUTUBE_REFRESH_TOKEN")

    if not all([client_id, client_secret, refresh_token]):
        print("❌ CRITICAL: YouTube API Secrets are missing!")
        return

    # API Authentication
    creds = Credentials(
        token=None,
        refresh_token=refresh_token,
        token_uri="https://oauth2.googleapis.com/token",
        client_id=client_id,
        client_secret=client_secret,
        scopes=["https://www.googleapis.com/auth/youtube"]
    )
    youtube = build("youtube", "v3", credentials=creds)

    # 🌟 ৭টি মেগা প্লেলিস্টের নাম এবং চমৎকার SEO ডেসক্রিপশন
    playlists_data = [
        {
            "title": "হাসির ও মজার কার্টুন 🤣 (Funny Cartoons)",
            "description": "ToonMagic Bangla-র সেরা সব হাসির কার্টুন ও মজার গল্প! বাচ্চাদের বিনোদনের জন্য দারুণ সব হাস্যকৌতুক ও মজার ঘটনা নিয়ে তৈরি আমাদের এই 3D অ্যানিমেশন ভিডিওগুলো। #FunnyCartoon #BanglaCartoon"
        },
        {
            "title": "শিক্ষামূলক ও নীতিকথা 📚 (Moral Stories)",
            "description": "ছোটদের জন্য দারুণ সব শিক্ষামূলক গল্প ও নীতিকথা। সততা, পরোপকার এবং জীবনের গুরুত্বপূর্ণ শিক্ষাগুলো আনন্দদায়ক 3D কার্টুনের মাধ্যমে তুলে ধরা হয়েছে। #MoralStories #BanglaGolpo"
        },
        {
            "title": "রূপকথা ও জাদুকরী গল্প ✨ (Fairy Tales)",
            "description": "রাজা-রানী, জাদুকর, পরি এবং জাদুকরী রাজ্যের সব রোমাঞ্চকর রূপকথার গল্প! বাচ্চাদের কল্পনার জগৎকে আরও সুন্দর করতে দেখুন আমাদের জাদুকরী অ্যানিমেশন। #FairyTales #RupkotharGolpo"
        },
        {
            "title": "ইসলামিক শিক্ষামূলক গল্প 🕌 (Islamic Stories)",
            "description": "সুন্দর ইসলামিক আদর্শ, নবী-রাসূলদের জীবনের শিক্ষামূলক ঘটনা এবং হাদিসের আলোকে তৈরি ছোটদের জন্য বিশেষ কার্টুন গল্প। #IslamicStories #BanglaIslamicCartoon"
        },
        {
            "title": "পশুপাখিদের মজার গল্প 🐾 (Animal Stories)",
            "description": "চালাক শিয়াল, বোকা কুমির, বুদ্ধিমান কাক এবং আরও অনেক পশুপাখির মজার ও শিক্ষণীয় গল্প। টুনি ও অন্যান্য পাখিদের দারুণ সব অ্যানিমেশন। #AnimalStories #TuniCartoon"
        },
        {
            "title": "অ্যাডভেঞ্চার ও সাই-ফাই 🚀 (Adventure & Sci-Fi)",
            "description": "সুপারহিরোদের সাহসিকতা, মহাকাশ ভ্রমণ এবং টাইম ট্রাভেলের মতো দুর্দান্ত সব অ্যাডভেঞ্চার গল্প! সায়েন্স ফিকশন ও রোমাঞ্চ ভালোবাসে এমন বাচ্চাদের জন্য। #Adventure #SciFiCartoon"
        },
        {
            "title": "ভুতের ও রহস্যের গল্প 👻 (Ghost & Mystery)",
            "description": "ভয়ংকর নয়, বরং গা ছমছমে মজার সব ভূতের ও রহস্যময় গল্প! বাচ্চাদের হাসাতে ও একটুখানি চমকে দিতে দারুণ সব 3D অ্যানিমেশন। #GhostStory #BhooterGolpo"
        }
    ]

    print("\n📝 Playlist Creation Results:\n" + "="*50)
    
    # প্লেলিস্ট তৈরি করা এবং ID প্রিন্ট করা
    for pl in playlists_data:
        try:
            body = {
                "snippet": {
                    "title": pl["title"],
                    "description": pl["description"]
                },
                "status": {
                    "privacyStatus": "public" # প্লেলিস্ট পাব্লিক থাকবে
                }
            }
            
            request = youtube.playlists().insert(part="snippet,status", body=body)
            response = request.execute()
            
            playlist_id = response['id']
            print(f'✅ Created: "{pl["title"]}"')
            print(f'🔗 ID: {playlist_id}\n')
            
        except Exception as e:
            print(f'❌ Failed to create "{pl["title"]}": {e}\n')

    print("="*50)
    print("🎯 COPY THE IDS ABOVE AND PASTE THEM INTO main.py 'playlist_map'")

if __name__ == "__main__":
    create_youtube_playlists()
