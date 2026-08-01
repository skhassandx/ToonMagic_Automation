import os
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

def upload_to_youtube_headless(video_path):
    client_id = os.environ.get("YOUTUBE_CLIENT_ID")
    client_secret = os.environ.get("YOUTUBE_CLIENT_SECRET")
    refresh_token = os.environ.get("YOUTUBE_REFRESH_TOKEN")

    if not all([client_id, client_secret, refresh_token]):
        print("⚠️ YouTube OAuth credentials missing in secrets. Skipping upload.")
        return None

    creds = Credentials(
        token=None,
        refresh_token=refresh_token,
        token_uri="https://oauth2.googleapis.com/token",
        client_id=client_id,
        client_secret=client_secret,
        scopes=["https://www.googleapis.com/auth/youtube.upload"]
    )

    creds.refresh(Request())
    youtube = build("youtube", "v3", credentials=creds)

    title = 'টুটুল ও জাদুর পেন্সিলের কাণ্ড! 🦖🎨 #Shorts #ToonMagicBangla'
    description = '''
দুষ্টু ছেলে টুটুল জাদুর পেন্সিল দিয়ে কুমির এঁকে নিজেই বিপদে পড়ে গেল! মজাদার 3D বাংলা কার্টুন গল্প।

চ্যানেলটি সাবস্ক্রাইব করে সাথেই থাকুন! ❤️

#Shorts #BanglaCartoon #3DAnimation #MoralStory #KidsCartoonBangla #ToonMagicBangla #BanglaGolpo
'''.strip()

    request_body = {
        'snippet': {
            'categoryId': '1', # Film & Animation
            'title': title,
            'description': description,
            'tags': ['shorts', 'bangla cartoon', '3d cartoon', 'ai animation', 'kids story', 'toonmagic bangla']
        },
        'status': {
            'privacyStatus': 'public',
            'selfDeclaredMadeForKids': False
        }
    }

    media_file = MediaFileUpload(video_path, chunksize=-1, resumable=True)
    request = youtube.videos().insert(
        part='snippet,status',
        body=request_body,
        media_body=media_file
    )

    response = request.execute()
    video_url = f"https://youtube.com/shorts/{response['id']}"
    print(f"🎉 YouTube Shorts Uploaded Headlessly! Link: {video_url}")
    return video_url