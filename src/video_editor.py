import os
import json
from moviepy.editor import VideoFileClip, AudioFileClip, concatenate_videoclips
import moviepy.video.fx.all as vfx
from config.settings import AUDIO_DIR, ANIMATED_DIR, FINAL_DIR

def create_final_videos(story_path):
    with open(story_path, 'r', encoding='utf-8') as f:
        story_data = json.load(f)

    processed_clips = []
    
    for scene in story_data['scenes']:
        scene_num = scene['scene_number']
        vid_path = os.path.join(ANIMATED_DIR, f"scene_{scene_num}.mp4")
        aud_path = os.path.join(AUDIO_DIR, f"scene_{scene_num}.mp3")

        if os.path.exists(vid_path) and os.path.exists(aud_path):
            v_clip = VideoFileClip(vid_path)
            a_clip = AudioFileClip(aud_path)

            if v_clip.duration < a_clip.duration:
                v_clip = v_clip.loop(duration=a_clip.duration).set_audio(a_clip)
            else:
                v_clip = v_clip.subclip(0, a_clip.duration).set_audio(a_clip)

            processed_clips.append(v_clip)

    if not processed_clips:
        print("⚠️ No clips found to merge.")
        return None, None

    full_video_path = os.path.join(FINAL_DIR, "FINAL_CARTOON_MOVIE.mp4")
    shorts_video_path = os.path.join(FINAL_DIR, "FINAL_CARTOON_SHORTS.mp4")

    # Merge full horizontal video
    full_movie = concatenate_videoclips(processed_clips, method="compose")
    full_movie.write_videofile(full_video_path, codec='libx264', audio_codec='aac', fps=24)

    # Convert to 9:16 Shorts
    w, h = full_movie.size
    target_w = int(h * 9 / 16)
    cropped_shorts = full_movie.fx(vfx.crop, width=target_w, height=h, x_center=w/2, y_center=h/2)
    cropped_shorts.write_videofile(shorts_video_path, codec='libx264', audio_codec='aac', fps=24)

    print("🎉 Full video & Shorts generated successfully!")
    return full_video_path, shorts_video_path