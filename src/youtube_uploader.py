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
            
        title = story_data.get('title', 'বাংলা মজার কার্টুন')
        
        # গল্পের প্রথম লাইনটি নিয়ে ডেসক্রিপশনে দেওয়ার জন্য এক্সট্র্যাক্ট করা
        first_scene = ""
        if 'scenes' in story_data and len(story_data['scenes']) > 0:
            first_scene = story_data['scenes'][0].get('narration', '')
            
        video_title = f"{title} ✨ | Bangla Cartoon | #Shorts"
        
        # এসইও (SEO) ফ্রেন্ডলি ডেসক্রিপশন তৈরি
        video_desc = f"""{title} - সম্পূর্ণ নতুন বাংলা কার্টুন গল্প।

গল্পের সারাংশ:
{first_scene} জানতে হলে ভিডিওটি শেষ পর্যন্ত দেখুন! 

ছোটদের জন্য দারুণ শিক্ষণীয় এবং মজার এই 3D অ্যানিমেশন কার্টুন। আমাদের চ্যানেলে প্রতিদিন নতুন নতুন রূপকথার গল্প, ভূতের গল্প এবং মজার কার্টুন আপলোড করা হয়। 

👉 সাবস্ক্রাইব করে আমাদের সাথেই থাকুন!

#BanglaCartoon #BengaliFairyTales #ToonMagicBangla #KidsCartoon #BanglaGolpo #MoralStories #3DAnimation #Shorts #CartoonBangla #RupkotharGolpo #BengaliStories
"""
        
        print(f"📺 Uploading Video: {video_title}")
        
        # হাই-ভলিউম সার্চ ট্যাগ যুক্ত করা হলো
        tags_list = [
            'bangla cartoon', 'cartoon bangla', 'bengali fairy tales', 
            'rupkothar golpo', 'bangla golpo', 'moral stories in bengali', 
            'kids cartoon', '3d animation bangla', 'toonmagic', 'shorts feed', 
            'trending shorts'
        ]
        
        body = {
            'snippet': {
                'title': video_title,
                'description': video_desc,
                'tags': tags_list,
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
