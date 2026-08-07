import os
import datetime
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.oauth2.credentials import Credentials

# 🌟 আপনার ৭টি প্লেলিস্টের রিয়েল আইডি (Smart Dictionary)
PLAYLISTS = {
    "moral": "PLZU3yfpAHzEM",      # শিক্ষামূলক ও নীতিকথা 📚
    "ghost": "PLOSv98OMol24",      # ভুতের ও রহস্যের গল্প 👻
    "adventure": "PLAuLcFlAf_Jo",  # অ্যাডভেঞ্চার ও সাই-ফাই 🚀
    "animal": "PLRYQPRJmPGkM",     # পশুপাখিদের মজার গল্প 🐾
    "islamic": "PLJQRqIqH37EY",    # ইসলামিক শিক্ষামূলক গল্প 🕌
    "funny": "PLTM7bJwT8Rv8",      # হাসির ও মজার কার্টুন 🤣
    "fairy": "PLccn5jUqTKAk"       # রূপকথা ও জাদুকরী গল্প ✨ (Default)
}

# 🧠 স্মার্ট অটো-ক্যাটাগরি ডিটেক্টর ফাংশন
def auto_detect_playlist(title, description):
    text = (title + " " + description).lower()
    
    # গল্পের শব্দ স্ক্যান করে সঠিক প্লেলিস্ট বাছাই
    if any(word in text for word in ["ভূত", "ghost", "ভয়ংকর", "রহস্য", "bhoot", "bhut", "scary"]):
        return PLAYLISTS["ghost"], "ভুতের ও রহস্যের গল্প 👻"
    elif any(word in text for word in ["ইসলাম", "নবী", "আল্লাহ", "islamic", "হাদিস", "islam", "muslim"]):
        return PLAYLISTS["islamic"], "ইসলামিক শিক্ষামূলক গল্প 🕌"
    elif any(word in text for word in ["পশু", "পাখি", "animal", "শিয়াল", "বাঘ", "টুনি", "কাক", "fox", "bird"]):
        return PLAYLISTS["animal"], "পশুপাখিদের মজার গল্প 🐾"
    elif any(word in text for word in ["মজা", "হাসি", "funny", "কমেডি", "mojar", "hasi"]):
        return PLAYLISTS["funny"], "হাসির ও মজার কার্টুন 🤣"
    elif any(word in text for word in ["অ্যাডভেঞ্চার", "মহাকাশ", "adventure", "sci-fi", "এলিয়েন", "space", "magic"]):
        return PLAYLISTS["adventure"], "অ্যাডভেঞ্চার ও সাই-ফাই 🚀"
    elif any(word in text for word in ["শিক্ষা", "নীতি", "moral", "উপদেশ", "shikkha", "niti"]):
        return PLAYLISTS["moral"], "শিক্ষামূলক ও নীতিকথা 📚"
    else:
        # কোনো স্পেসিফিক ক্যাটাগরি না পেলে ডিফল্ট হিসেবে 'রূপকথা' তে যাবে
        return PLAYLISTS["fairy"], "রূপকথা ও জাদুকরী গল্প ✨"

def upload_to_youtube(video_path, title, description, provided_playlist_id=None):
    print("🚀 Uploading to YouTube with 100% Best SEO, Auto-Playlist Routing & Location...")
    
    client_id = os.environ.get("YOUTUBE_CLIENT_ID")
    client_secret = os.environ.get("YOUTUBE_CLIENT_SECRET")
    refresh_token = os.environ.get("YOUTUBE_REFRESH_TOKEN")

    if not all([client_id, client_secret, refresh_token]):
        raise Exception("❌ CRITICAL: YouTube API Secrets (Client ID, Secret, or Refresh Token) are missing in GitHub!")

    try:
        creds = Credentials(
            token=None,
            refresh_token=refresh_token,
            token_uri="https://oauth2.googleapis.com/token",
            client_id=client_id,
            client_secret=client_secret,
            scopes=["https://www.googleapis.com/auth/youtube.upload", "https://www.googleapis.com/auth/youtube"]
        )

        youtube = build("youtube", "v3", credentials=creds)
        today_iso = datetime.datetime.utcnow().isoformat() + 'Z'

        # 🌟 হাইলি টপ এসইও ট্যাগ (৪৫০ ক্যারেক্টারের মধ্যে সবচেয়ে পাওয়ারফুল কিওয়ার্ড)
        viral_tags = [
            "bangla cartoon", "bangla golpo", "bengali fairy tales", "cartoon bangla",
            "kids cartoon", "rupkothar golpo", "shorts feed", "trending shorts",
            "bangla moral stories", "tunir golpo", "bengali stories", "bangla animation",
            "shialer golpo", "bhooter golpo", "bangla cartoon 2026", "bangla short film",
            "chotoder golpo", "bengali cartoon", "bangla mojar golpo", "fairy tales in bengali",
            "animal cartoon bangla", "notun bangla golpo", "bangla golpo cartoon", 
            "bangla fairy tales new", "3d animation bangla", "mojar cartoon bangla", "thakurmar jhuli"
        ]

        # 🌟 স্মার্ট ডাইনামিক টাইটেল (ইউটিউব লিমিট ১০০ ক্যারেক্টারের মধ্যে সেফ রাখা হলো)
        final_title = f"{title[:70]} ✨ | Bangla Cartoon #Shorts"
        
        # 🌟 প্রফেশনাল ও হাই-র‍্যাংকিং এসইও ডেসক্রিপশন
        final_description = f"""{description}

আজকের দারুণ মজার বাংলা কার্টুন গল্পে আপনাদের স্বাগতম! 🌟 আমাদের 'ToonMagic Bangla' চ্যানেলে আমরা প্রতিদিন নতুন শিক্ষামূলক, মজার এবং রূপকথার জাদুকরী গল্প নিয়ে আসি। 3D অ্যানিমেশন গল্পগুলো শুধু আনন্দই দেয় না, বরং ভালো শিক্ষাও দেয়। 

ভিডিওটি ভালো লাগলে অবশ্যই লাইক দিন, বন্ধুদের সাথে শেয়ার করুন এবং আমাদের চ্যানেলটি সাবস্ক্রাইব করে বেল আইকনটি বাজিয়ে দিন! 

🔥 Top Queries Solved in This Video:
- Bangla Cartoon 2026
- Rupkothar Golpo Shorts
- Thakurmar Jhuli Animation
- Bengali Fairy Tales New
- Bangla Moral Stories

#BanglaCartoon #BengaliFairyTales #BanglaGolpo #MoralStories #Shorts #ToonMagicBangla #KidsCartoon #RupkotharGolpo #BengaliStory
"""

        # 🌟 লোকেশন সেটআপ (বাংলাদেশ)
        location_details = {
            "latitude": 23.8103,
            "longitude": 90.4125,
            "description": "Bangladesh"
        }

        body = {
            'snippet': {
                'title': final_title,
                'description': final_description,
                'tags': viral_tags,
                'categoryId': '1', # Film & Animation
                'defaultLanguage': 'bn',
                'defaultAudioLanguage': 'bn'
            },
            'status': {
                'privacyStatus': 'public',
                'madeForKids': False,               
                'selfDeclaredMadeForKids': False    
            },
            'recordingDetails': {
                'recordingDate': today_iso,
                'location': location_details
            }
        }

        # 📤 ভিডিও আপলোড প্রসেস
        media = MediaFileUpload(video_path, chunksize=-1, resumable=True, mimetype='video/mp4')
        request = youtube.videos().insert(part="snippet,status,recordingDetails", body=body, media_body=media)
        
        response = request.execute()
        video_id = response.get('id')
        
        print(f"✅ BINGO! Video Successfully Uploaded! URL: https://youtu.be/{video_id}")

        # 🧠 অটো-ডিটেক্ট প্লেলিস্ট লজিক কল করা
        target_playlist_id, playlist_name = auto_detect_playlist(title, description)

        # 📂 ভিডিওটি শুধুমাত্র নির্বাচিত নির্দিষ্ট প্লেলিস্টে যুক্ত করা
        try:
            print(f"📂 Auto-routing video to category: {playlist_name} (ID: {target_playlist_id})...")
            playlist_body = {
                'snippet': {
                    'playlistId': target_playlist_id,
                    'resourceId': {
                        'kind': 'youtube#video',
                        'videoId': video_id
                    }
                }
            }
            youtube.playlistItems().insert(part="snippet", body=playlist_body).execute()
            print(f"✅ Video successfully saved ONLY to '{playlist_name}' playlist!")
        except Exception as e:
            print(f"⚠️ Video uploaded, but failed to add to playlist '{playlist_name}': {e}")

        return video_id

    except Exception as e:
        print(f"❌ YouTube Upload Failed: {e}")
        raise e
