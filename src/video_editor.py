import os
import json
from moviepy.editor import ImageClip, AudioFileClip, concatenate_videoclips
from config.settings import IMAGES_DIR, AUDIO_DIR, FINAL_VIDEOS_DIR

def create_final_videos(story_path):
    with open(story_path, 'r', encoding='utf-8') as f:
        story_data = json.load(f)
        
    total_scenes = len(story_data.get('scenes', []))
    video_clips = []
    
    for i in range(1, total_scenes + 1):
        img_path = os.path.join(IMAGES_DIR, f"scene_{i}.jpg")
        aud_path = os.path.join(AUDIO_DIR, f"scene_{i}.mp3")
        
        if os.path.exists(img_path) and os.path.exists(aud_path):
            audio_clip = AudioFileClip(aud_path)
            
            # ইমেজ লোড করে অডিওর সমান লম্বা করা
            img_clip = ImageClip(img_path).set_duration(audio_clip.duration)
            
            # সিনেমাটিক জুম-ইন ইফেক্ট (অ্যানিমেশন)
            # এটি ছবিটিকে আস্তে আস্তে ১০% জুম করবে, ফলে ভিডিওটি জীবন্ত মনে হবে
            def zoom_effect(t):
                return 1 + 0.1 * (t / img_clip.duration)
                
            img_clip = img_clip.resize(zoom_effect)
            
            # ফাইনাল সাইজ 1080x1920 নিশ্চিত করা এবং ক্রপ করা
            img_clip = img_clip.crop(x_center=img_clip.w/2, y_center=img_clip.h/2, width=1080, height=1920)
            img_clip = img_clip.set_audio(audio_clip)
            
            video_clips.append(img_clip)
            
    if not video_clips:
        print("⚠️ No clips found to merge.")
        return None, None

    print(f"🎬 Merging {len(video_clips)} scenes with Cinematic Zoom Animation...")
    final_clip = concatenate_videoclips(video_clips, method="compose")
    
    shorts_path = os.path.join(FINAL_VIDEOS_DIR, "FINAL_CARTOON_SHORTS.mp4")
    
    # হাই বিটরেটে রেন্ডার
    final_clip.write_videofile(
        shorts_path, 
        fps=24, 
        codec="libx264", 
        audio_codec="aac", 
        bitrate="8000k",
        preset="ultrafast",
        verbose=False, 
        logger=None
    )
    
    final_clip.close()
    
    print("🎉 Cinematic Animated Shorts Generated Successfully!")
    return shorts_path, shorts_path
