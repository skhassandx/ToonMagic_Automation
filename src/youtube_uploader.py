import os
import datetime
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.oauth2.credentials import Credentials

# 🌟 প্লেলিস্ট অ্যাড করার জন্য playlist_id=None প্যারামিটার যুক্ত করা হয়েছে
def upload_to_youtube(video_path, title, description, playlist_id=None):
    print("🚀 Uploading to YouTube with Full SEO Optimization (Comments ON)...")
    
    client_id = os.environ.get("YOUTUBE_CLIENT_ID")
    client_secret = os.environ.get("YOUTUBE_CLIENT_SECRET")
    refresh_token = os.environ.get("YOUTUBE_REFRESH_TOKEN")

    if not all([client_id, client_secret, refresh_token]):
        # 🌟 আপনার দেওয়া হুবহু সেই লাইন
        raise Exception("❌ CRITICAL: YouTube API Secrets (Client ID, Secret, or Refresh Token) are missing in GitHub!")

    try:
        # 🌟 ম্যাজিক ট্রিক: Scopes যুক্ত করা হলো, যাতে ['https' এরর আর না আসে
        # (প্লেলিস্টের জন্য youtube স্কোপটিও যুক্ত করা হলো)
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

        # 🌟 পাওয়ারফুল ট্যাগ (প্রায় ৪০০ ক্যারেক্টার)
        viral_tags = [
            "bangla cartoon", "bangla golpo", "bengali fairy tales", 
            "cartoon bangla", "kids cartoon", "rupkothar golpo", 
            "bangla moral stories", "bengali stories", "bangla animation",
            "thakurmar jhuli", "shorts feed", "trending shorts",
            "bhuter golpo", "tuntuni golpo", "bangla mojar cartoon", 
            "notun bangla golpo", "shishuder golpo", "bangla cartoon 2026", 
            "animated stories bangla", "bengali kids video", 
            "bangla short film", "bengali folk tales", "toonmagic bangla"
        ]

        # 🌟 বিশাল এবং প্রফেশনাল ডেসক্রিপশন
        seo_description = f"""{description}

আজকের দারুণ মজার বাংলা কার্টুন গল্পে আপনাদের স্বাগতম! 🌟 আমাদের 'ToonMagic Bangla' চ্যানেলে আমরা প্রতিদিন নতুন শিক্ষামূলক, মজার এবং রূপকথার জাদুকরী গল্প নিয়ে আসি। 3D অ্যানিমেশন গল্পগুলো শুধু আনন্দই দেয় না, বরং ভালো শিক্ষাও দেয়। 

ভিডিওটি ভালো লাগলে অবশ্যই লাইক দিন, বন্ধুদের সাথে শেয়ার করুন এবং আমাদের চ্যানেলটি সাবস্ক্রাইব করে বেল আইকনটি বাজিয়ে দিন! আপনার মূল্যবান মতামত অবশ্যই কমেন্ট করে জানাবেন।

Welcome to ToonMagic Bangla! Enjoy our latest 3D animated Bengali fairy tales and moral stories. Don't forget to subscribe!

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
                'title': f"{title} ✨ | Bangla Cartoon | #Shorts",
                'description': seo_description,
                'tags': viral_tags,
                'categoryId': '1', # Film & Animation
                'defaultLanguage': 'bn',
                'defaultAudioLanguage': 'bn'
            },
            'status': {
                'privacyStatus': 'public',
                'madeForKids': False,               # 🌟 কমেন্ট অন রাখার জন্য False
                'selfDeclaredMadeForKids': False    # 🌟 কমেন্ট অন রাখার জন্য False
            },
            'recordingDetails': {
                'recordingDate': today_iso,
                'location': location_details
            }
        }

        media = MediaFileUpload(video_path, chunksize=-1, resumable=True, mimetype='video/mp4')
        request = youtube.videos().insert(part="snippet,status,recordingDetails", body=body, media_body=media)
        
        response = request.execute()
        video_id = response.get('id')
        
        # 🌟 আপনার দেওয়া BINGO লাইনটি রেখে URL যুক্ত করা হলো
        print(f"✅ BINGO! Video Successfully Uploaded & Published! URL: https://youtu.be/{video_id}")

        # 🌟 প্লেলিস্টে যুক্ত করার লজিক
        if playlist_id:
            try:
                print(f"📂 Adding video to Playlist ID: {playlist_id}...")
                playlist_body = {
                    'snippet': {
                        'playlistId': playlist_id,
                        'resourceId': {
                            'kind': 'youtube#video',
                            'videoId': video_id
                        }
                    }
                }
                youtube.playlistItems().insert(part="snippet", body=playlist_body).execute()
                print("✅ Video added to the playlist successfully!")
            except Exception as e:
                print(f"⚠️ Video uploaded, but failed to add to playlist: {e}")

        return video_id

    except Exception as e:
        print(f"❌ YouTube Upload Failed: {e}")
        raise e
