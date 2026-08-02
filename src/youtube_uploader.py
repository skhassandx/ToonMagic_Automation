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
        
        story_path = os.path.join(STORIES_DIR, "latest_story.json")
        with open(story_path, 'r', encoding='utf-8') as f:
            story_data = json.load(f)
            
        title = story_data.get('title', 'মজার বাংলা কার্টুন গল্প')
        dynamic_tags = story_data.get('tags', [])
        
        base_tags = [
            'bangla cartoon', 'cartoon bangla', 'bengali fairy tales', 
            'rupkothar golpo', 'bangla golpo', 'kids cartoon', 'shorts feed', 'trending shorts'
        ]
        
        all_tags = list(set(dynamic_tags + base_tags))
        
        first_scene = ""
        if 'scenes' in story_data and len(story_data['scenes']) > 0:
            first_scene = story_data['scenes'][0].get('narration', '')
            
        video_title = f"{title} ✨ | Bangla Cartoon | #Shorts"
        
        video_desc = f"""{title} - সম্পূর্ণ নতুন বাংলা কার্টুন গল্প।

গল্পের সারাংশ:
{first_scene} 

সম্পূর্ণ কাহিনী জানতে ভিডিওটি শেষ পর্যন্ত দেখুন! 

👉 চ্যানেলটি সাবস্ক্রাইব করে বেল আইকনটি প্রেস করে রাখুন!

#BanglaCartoon #BengaliFairyTales #ToonMagicBangla #KidsCartoon #BanglaGolpo #Shorts #{title.replace(' ', '')}
"""
        
        print(f"📺 Uploading Video Title: {video_title}")
        
        body = {
            'snippet': {
                'title': video_title,
                'description': video_desc,
                'tags': all_tags,
                'categoryId': '1' # Film & Animation
            },
            'status': {
                'privacyStatus': 'public',
                'madeForKids': False  # Made for kids বন্ধ করা হলো যেন কমেন্ট ও রিচ চালু থাকে
            }
        }
        
        media = MediaFileUpload(video_path, chunksize=-1, resumable=True)
        request = youtube.videos().insert(part=','.join(body.keys()), body=body, media_body=media)
        
        response = None
        while response is None:
            status, response = request.next_chunk()
            if status:
                print(f"⏳ Uploading... {int(status.progress() * 100)}%")
                
        print(f"✅ YouTube Shorts Uploaded Successfully! Link: https://youtube.com/shorts/{response['id']}")
        
    except Exception as e:
        print(f"❌ YouTube Upload Error: {e}")
