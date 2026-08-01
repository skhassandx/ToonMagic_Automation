import os
import json
import google.auth
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from config.settings import STORIES_DIR

def upload_to_youtube_headless(video_path):
    print("📡 Authenticating with YouTube...")
    
    client_id = os.environ.get('YOUTUBE_CLIENT_ID')
    client_secret = os.environ.get('YOUTUBE_CLIENT_SECRET')
    refresh_token = os.environ.get('YOUTUBE_REFRESH_TOKEN')

    if not all([client_id, client_secret, refresh_token]):
        print("❌ YouTube API credentials missing in GitHub Secrets!")
        return

    creds = Credentials(
        token=None,
        refresh_token=refresh_token,
        token_uri="https://oauth2.googleapis.com/token",
        client_id=client_id,
        client_secret=client_secret
    )

    try:
        youtube = build('youtube', 'v3', credentials=creds)
        
        # জেমিনাইয়ের তৈরি করা গল্পের JSON ফাইল থেকে নাম পড়া
        story_path = os.path.join(STORIES_DIR, "latest_story.json")
        with open(story_path, 'r', encoding='utf-8') as f:
            story_data = json.load(f)
            
        # গল্পের টাইটেলটিই ইউটিউবের টাইটেল হিসেবে সেট করা
        video_title = f"{story_data.get('title', 'বাংলা মজার কার্টুন')} ✨ #Shorts #CartoonBangla"
        video_desc = f"{story_data.get('title')} - সম্পূর্ণ নতুন বাংলা কার্টুন গল্প।\n\n#BanglaCartoon #MoralStories #ToonMagicBangla #KidsVideo"
        
        print(f"📺 Uploading Video: {video_title}")
        
        body = {
            'snippet': {
                'title': video_title,
                'description': video_desc,
                'tags': ['bangla cartoon', 'cartoon bangla', 'moral stories', 'kids video', 'animation', 'shorts'],
                'categoryId': '1' # Film & Animation
            },
            'status': {
                'privacyStatus': 'public',
                'madeForKids': True
            }
        }
        
        media = MediaFileUpload(video_path, chunksize=-1, resumable=True)
        request = youtube.videos().insert(part=','.join(body.keys()), body=body, media_body=media)
        
        response = None
        while response is None:
            status, response = request.next_chunk()
            if status:
                print(f"⏳ Uploading... {int(status.progress() * 100)}%")
                
        print(f"✅ YouTube Shorts Uploaded! Link: https://youtube.com/shorts/{response['id']}")
        
    except Exception as e:
        print(f"❌ YouTube Upload Error: {e}")
