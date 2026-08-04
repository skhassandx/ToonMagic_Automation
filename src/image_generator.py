import os
import json
import time
from huggingface_hub import InferenceClient
from config.settings import IMAGES_DIR

def generate_images(story_path):
    with open(story_path, 'r', encoding='utf-8') as f:
        story_data = json.load(f)

    api_key = os.environ.get("HF_API_KEY")
    if not api_key:
        print("❌ CRITICAL ERROR: HF_API_KEY not found in environment variables!")
        return False

    # 🌟 অফিশিয়াল SDK ব্যবহার করা হলো, যা অটোমেটিকভাবে রাউটিং হ্যান্ডেল করবে
    client = InferenceClient(token=api_key)
    images_success = True

    for scene in story_data['scenes']:
        scene_num = scene['scene_number']
        img_path = os.path.join(IMAGES_DIR, f"scene_{scene_num}.jpg")

        if os.path.exists(img_path):
            continue

        prompt = scene.get('image_prompt', "A cartoon bear")
        # 🌟 প্রফেশনাল প্রম্পট
        enhanced_prompt = f"3D Pixar style, highly detailed, {prompt}, wide angle shot, full body, cinematic lighting, 8k resolution"
        
        print(f"🎨 Generating Image for Scene {scene_num} using Hugging Face SDK...")

        image_downloaded = False
        
        for attempt in range(3):
            try:
                # 🌟 SDK নিজে থেকেই লেটেস্ট সার্ভারে কানেক্ট করে ছবি আনবে
                image = client.text_to_image(
                    enhanced_prompt,
                    model="stabilityai/stable-diffusion-xl-base-1.0"
                )
                image.save(img_path)
                print(f"✅ Scene {scene_num} image saved successfully!")
                image_downloaded = True
                break
            except Exception as e:
                print(f"⚠️ Image generation failed on attempt {attempt+1}: {e}")
                time.sleep(10)

        if not image_downloaded:
            print(f"❌ CRITICAL ERROR: Failed to generate image for Scene {scene_num}")
            images_success = False
            break

    return images_success
