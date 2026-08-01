# ToonMagic Bangla - Fully Automated AI Cartoon Channel Pipeline 🚀

This repository automatically generates 3D animated Bengali cartoon stories, renders scenes using AI (Replicate Minimax), creates 9:16 vertical YouTube Shorts, and automatically uploads them to your YouTube channel on a schedule.

## 📂 Repository Structure

```
ToonMagic_Automation_Project/
├── .github/
│   └── workflows/
│       └── auto_cartoon.yml       # GitHub Actions Cron Workflow Schedule
├── config/
│   └── settings.py               # Path & Directory settings
├── src/
│   ├── story_generator.py        # Story & TTS audio generation
│   ├── video_generator.py        # Replicate API Minimax video renderer
│   ├── video_editor.py           # Video merger & 9:16 Shorts converter
│   └── youtube_uploader.py       # Headless YouTube Upload via Refresh Token
├── utils/
│   └── get_refresh_token.py      # Helper script to generate YouTube Refresh Token ONCE
├── backup/                        # Backups directory (automatically committed to Git)
│   ├── stories/
│   ├── images/
│   ├── audio/
│   ├── animated_scenes/
│   └── final_videos/
├── main.py                       # Main pipeline executor
├── requirements.txt              # Dependencies
└── README.md
```

## 🔑 Setup GitHub Secrets (One Time Only)

Go to your GitHub Repository -> **Settings** -> **Secrets and variables** -> **Actions** -> **New repository secret**:

1. `REPLICATE_API_TOKEN`: Your Replicate API token (`r8_LZE...`)
2. `YOUTUBE_CLIENT_ID`: From Google Cloud OAuth Client ID
3. `YOUTUBE_CLIENT_SECRET`: From Google Cloud OAuth Client Secret
4. `YOUTUBE_REFRESH_TOKEN`: Generated using `python utils/get_refresh_token.py`