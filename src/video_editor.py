import os
import json
from moviepy.editor import VideoFileClip, AudioFileClip, concatenate_videoclips
from config.settings import ANIMATED_DIR, AUDIO_DIR, FINAL_VIDEOS_DIR, STORIES_DIR

def create_final_videos(story_path):
    with open(story_path, 'r', encoding='utf-8') as f:
        story_data = json.load(f)
        
    total_scenes = len(story_data.get('scenes', []))
    video_clips = []
    
    for i in range(1, total_scenes + 1):
        vid_path = os.path.join(ANIMATED_DIR, f"scene_{i}.mp4")
        aud_path = os.path.join(AUDIO_DIR, f"scene_{i}.mp3")
        
        if os.path.exists(vid_path) and os.path.exists(aud_path):
            v_clip = VideoFileClip(vid_path)
            a_clip = AudioFileClip(aud_path)
            
            v_clip = v_clip.set_duration(a_clip.duration)
            v_clip = v_clip.set_audio(a_clip)
            video_clips.append(v_clip)
            
    if not video_clips:
        print("⚠️ No clips found to merge.")
        return None, None

    print(f"🎬 Merging all {len(video_clips)} scenes into one Full Video...")
    final_clip = concatenate_videoclips(video_clips, method="compose")
    
    full_video_path = os.path.join(FINAL_VIDEOS_DIR, "FINAL_CARTOON_MOVIE.mp4")
    shorts_path = os.path.join(FINAL_VIDEOS_DIR, "FINAL_CARTOON_SHORTS.mp4")
    
    # যেহেতু ছবিগুলো আগে থেকেই 9:16, তাই ক্রপ করার দরকার নেই
    final_clip.write_videofile(full_video_path, fps=24, codec="libx264", audio_codec="aac", verbose=False, logger=None)
    final_clip.write_videofile(shorts_path, fps=24, codec="libx264", audio_codec="aac", verbose=False, logger=None)
    
    final_clip.close()
    
    print("🎉 Full video & Shorts generated successfully!")
    return full_video_path, shorts_path
