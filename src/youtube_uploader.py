import os
import datetime
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.oauth2.credentials import Credentials

def upload_to_youtube(video_path, title, description, playlist_id=None):
    print("🚀 Uploading to YouTube with Mega SEO Optimization & Video Location...")
    
    client_id = os.environ.get("YOUTUBE_CLIENT_ID")
    client_secret = os.environ.get("YOUTUBE_CLIENT_SECRET")
    refresh_token = os.environ.get("YOUTUBE_REFRESH_TOKEN")

    if not all([client_id, client_secret, refresh_token]):
        raise Exception("❌ CRITICAL: YouTube API Secrets are missing in GitHub!")

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
        today_iso = datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")

        # 🎯 ১. মেগা এসইও টাইটেল ও ডেসক্রিপশন মডিফিকেশন
        # টাইটেল আকর্ষণীয় এবং হ্যাশট্যাগ পারফেক্ট করা হলো
        optimized_title = "জাদুর শাঁখ ও স্ফটিক দৈত্য ✨ | Bangla Cartoon #Shorts #Viral"
        
        optimized_description = (
            "জাদুর শাঁখ ও স্ফটিক দৈত্যের এক রোমাঞ্চকর বাংলা রূপকথার গল্প! ✨\n\n"
            "Enjoy this amazing Bangla Cartoon Moral Story. If you love Bengali Fairy Tales and animated stories, "
            "make sure to subscribe for more new updates!\n\n"
            "🔥 Top Queries Solved:\n"
            "- Bangla Cartoon 2026\n"
            "- Rupkothar Golpo Shorts\n"
            "- Thakurmar Jhuli Animation\n"
            "- Bengali Fairy Tales New\n\n"
            "#banglacartoon #shorts #viralshorts #trending #fairy tales"
        )

        # 🎯 ২. ৪২০ ক্যারেক্টারের বেস্ট হাই-ভলিউম এসইও ট্যাগস
        viral_tags = [
            "bangla cartoon", "bangla golpo", "bengali fairy tales", "cartoon bangla", 
            "kids cartoon", "rupkothar golpo", "bangla moral stories", "bengali stories", 
            "bangla animation", "thakurmar jhuli", "shorts feed", "trending shorts",
            "bhuter golpo", "tuntuni golpo", "bangla mojar cartoon", "notun bangla golpo", 
            "shishuder golpo", "bangla cartoon 2026", "animated stories bangla", "bengali kids video"
        ]

        # 🎯 ৩. ভিডিও লোকেশন ফিক্স (Bangladesh জিপিএস লোকেশন)
        location_details = {
            "latitude": 23.6850,    # বাংলাদেশের ল্যাটিটিউড
            "longitude": 90.3563,   # বাংলাদেশের লঙ্গিটিউড
            "description": "Bangladesh"
        }

        body = {
            'snippet': {
                'title': optimized_title,
                'description': optimized_description,
                'tags': viral_tags,
                'categoryId': '1 film & Animation', # কার্টুনের জন্য বেস্ট ক্যাটাগরি
                'defaultLanguage': 'bn',
                'defaultAudioLanguage': 'bn'
            },
            'status': {
                'privacyStatus': 'public',
                'selfDeclaredMadeForKids': False
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
        
        print(f"✅ BINGO! Video Successfully Uploaded & Published! URL: https://youtu.be/{video_id}")

        # 🎯 ৪. সেফ প্লেলিস্ট অ্যাটাচমেন্ট (এরর হ্যান্ডলিং সহ)
        if playlist_id:
            try:
                print(f"📂 Attempting to add video to Playlist ID: {playlist_id}...")
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
            except Exception as playlist_error:
                print(f"⚠️ Playlist notice: Could not auto-add to playlist ({playlist_error}). Please check your playlist privacy or ID inside YouTube Studio manually.")

        return video_id

    except Exception as e:
        print(f"❌ YouTube Upload Failed: {e}")
        raise e
