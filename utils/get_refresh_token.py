# =======================================================
# Run this script ONCE locally or on Colab to get YOUTUBE_REFRESH_TOKEN
# =======================================================
import os
from google_auth_oauthlib.flow import InstalledAppFlow

SCOPES = ['https://www.googleapis.com/auth/youtube.upload']

def main():
    if not os.path.exists('client_secret.json'):
        print("❌ 'client_secret.json' file not found in current folder!")
        return

    flow = InstalledAppFlow.from_client_secrets_file(
        'client_secret.json', 
        scopes=SCOPES,
        redirect_uri='http://localhost'
    )
    
    auth_url, _ = flow.authorization_url(prompt='consent', access_type='offline')
    
    print("👉 1. Open this URL in browser and Allow access:
")
    print(auth_url)
    print("
👉 2. Paste the redirected localhost URL here:
")
    
    code_input = input("Paste URL here: ").strip()
    code = code_input.split("code=")[1].split("&")[0] if "code=" in code_input else code_input

    flow.fetch_token(code=code)
    creds = flow.credentials

    print("
================ SUCCESS! ================")
    print("Add these 3 values to your GitHub Repository Secrets:")
    print(f"YOUTUBE_CLIENT_ID: {creds.client_id}")
    print(f"YOUTUBE_CLIENT_SECRET: {creds.client_secret}")
    print(f"YOUTUBE_REFRESH_TOKEN: {creds.refresh_token}")
    print("==========================================")

if __name__ == '__main__':
    main()