import os
import datetime
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

def upload_video_to_youtube(youtube, video_path, title, description, playlist_id=None):
    print("🚀 Uploading video to YouTube with Pro SEO Settings...")

    # ১. আজকের রেকর্ডিং ডেট স্বয়ংক্রিয়ভাবে জেনারেট করা
    today_iso = datetime.datetime.utcnow().isoformat() + 'Z'

    # ২. প্রো-লেভেল ইউনিক ট্যাগ (প্রায় ৫০০ ক্যারেক্টার)
    viral_tags = [
        "bangla cartoon", "bangla golpo", "bengali fairy tales", "cartoon bangla",
        "kids cartoon", "rupkothar golpo", "shorts feed", "trending shorts",
        "bangla moral stories", "tunir golpo", "bengali stories", "bangla animation",
        "shialer golpo", "bhooter golpo", "bangla cartoon 2026", "bangla short film",
        "chotoder golpo", "bengali cartoon", "bangla mojar golpo", "fairy tales in bengali",
        "thakurmar jhuli", "bangla shorts cartoon", "notun bangla golpo", "animal cartoon bangla"
    ]

    # ৩. ভিডিওর মেটাডেটা এবং এসইও (SEO) সেটিংস
    request_body = {
        'snippet': {
            'title': title,
            'description': description,
            'tags': viral_tags,
            'categoryId': '1',  # 1 = Film & Animation
            'defaultLanguage': 'bn',       # ভিডিওর টাইটেল ও ডেসক্রিপশন ভাষা (Bangla)
            'defaultAudioLanguage': 'bn'   # অরিজিনাল অডিও ভাষা (Bangla)
        },
        'status': {
            'privacyStatus': 'public',  
            'madeForKids': True,        # কার্টুন যেহেতু, তাই Kids ফ্রেন্ডলি রাখা ভালো
            'selfDeclaredMadeForKids': True
        },
        'recordingDetails': {
            'recordingDate': today_iso  # আজকের রেকর্ডিং ডেট
        }
    }

    # ৪. ভিডিও আপলোড রিকোয়েস্ট
    media = MediaFileUpload(video_path, chunksize=-1, resumable=True, mimetype='video/mp4')
    request = youtube.videos().insert(
        part="snippet,status,recordingDetails",
        body=request_body,
        media_body=media
    )

    response = request.execute()
    video_id = response.get("id")
    print(f"✅ Video Uploaded Successfully! Video ID: {video_id}")

    # ৫. প্লেলিস্টে অ্যাড করা (যদি Playlist ID দেওয়া থাকে)
    if playlist_id and video_id:
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
            youtube.playlistItems().insert(
                part="snippet",
                body=playlist_body
            ).execute()
            print("✅ Video added to the playlist successfully!")
        except Exception as e:
            print(f"⚠️ Failed to add video to playlist: {e}")

    return video_id
