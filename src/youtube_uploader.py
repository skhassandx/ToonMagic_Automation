import os
import datetime
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.oauth2.credentials import Credentials

def upload_to_youtube(video_path, title, description):
    print("🚀 Uploading to YouTube with Full SEO Optimization...")
    
    client_id = os.environ.get("YOUTUBE_CLIENT_ID")
    client_secret = os.environ.get("YOUTUBE_CLIENT_SECRET")
    refresh_token = os.environ.get("YOUTUBE_REFRESH_TOKEN")

    if not all([client_id, client_secret, refresh_token]):
        raise Exception("❌ CRITICAL: YouTube API Secrets (Client ID, Secret, or Refresh Token) are missing in GitHub!")

    try:
        # 🌟 ম্যাজিক ট্রিক: Scopes যুক্ত করা হলো, যাতে ['https' এরর আর না আসে
        creds = Credentials(
            token=None,
            refresh_token=refresh_token,
            token_uri="https://oauth2.googleapis.com/token",
            client_id=client_id,
            client_secret=client_secret,
            scopes=["https://www.googleapis.com/auth/youtube.upload"]
        )

        youtube = build("youtube", "v3", credentials=creds)
        today_iso = datetime.datetime.utcnow().isoformat() + 'Z'

        viral_tags = [
            "bangla cartoon", "bangla golpo", "bengali fairy tales", "cartoon bangla",
            "kids cartoon", "rupkothar golpo", "shorts feed", "trending shorts",
            "bangla moral stories", "tunir golpo", "bengali stories", "bangla animation",
            "shialer golpo", "bhooter golpo", "bangla cartoon 2026", "bangla short film",
            "chotoder golpo", "bengali cartoon", "bangla mojar golpo", "fairy tales in bengali"
        ]

        body = {
            'snippet': {
                'title': f"{title} ✨ | Bangla Cartoon | #Shorts",
                'description': f"{description}\n\n#BanglaCartoon #MoralStories #Shorts",
                'tags': viral_tags,
                'categoryId': '1', # Film & Animation
                'defaultLanguage': 'bn',
                'defaultAudioLanguage': 'bn'
            },
            'status': {
                'privacyStatus': 'public',
                'madeForKids': True,
                'selfDeclaredMadeForKids': True
            },
            'recordingDetails': {
                'recordingDate': today_iso
            }
        }

        media = MediaFileUpload(video_path, chunksize=-1, resumable=True, mimetype='video/mp4')
        request = youtube.videos().insert(part="snippet,status,recordingDetails", body=body, media_body=media)
        
        response = request.execute()
        video_id = response.get('id')
        print(f"✅ BINGO! Video Successfully Uploaded & Published! Video ID: {video_id}")
        return video_id

    except Exception as e:
        print(f"❌ YouTube Upload Failed: {e}")
        raise e
