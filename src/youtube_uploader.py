import os
import datetime
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.oauth2.credentials import Credentials

def get_youtube_service():
    client_id = os.environ.get("YOUTUBE_CLIENT_ID")
    client_secret = os.environ.get("YOUTUBE_CLIENT_SECRET")
    refresh_token = os.environ.get("YOUTUBE_REFRESH_TOKEN")

    creds = Credentials(
        None,
        refresh_token=refresh_token,
        token_uri="[https://oauth2.googleapis.com/token](https://oauth2.googleapis.com/token)",
        client_id=client_id,
        client_secret=client_secret
    )
    return build("youtube", "v3", credentials=creds)

def upload_to_youtube(video_path, title, description):
    print("🚀 Uploading to YouTube with Full SEO Optimization...")
    youtube = get_youtube_service()

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
            'categoryId': '1',
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

    print(f"✅ Video Uploaded! Video ID: {response.get('id')}")
    return response.get('id')
