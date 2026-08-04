import os
import json
import time
from google import genai
from google.genai import types
from config.settings import IMAGES_DIR

def generate_images(story_path):
    with open(story_path, 'r', encoding='utf-8') as f:
        story_data = json.load(f)

    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("❌ CRITICAL ERROR: GEMINI_API_KEY not found!")
        return False

    client = genai.Client(api_key=api_key)
    images_success = True

    for scene in story_data['scenes']:
        scene_num = scene['scene_number']
        img_path = os.path.join(IMAGES_DIR, f"scene_{scene_num}.jpg")

        if os.path.exists(img_path):
            continue

        prompt = scene.get('image_prompt', "3D Pixar style cartoon")
        enhanced_prompt = f"3D Pixar animation style, {prompt}, masterpiece, highly detailed, vibrant colors, FULL BODY SHOT, WIDE ANGLE, centered in frame, zoomed out, showing full environment"
        
        print(f"🎨 Generating Image for Scene {scene_num} using Imagen 3...")

        try:
            # 🌟 সঠিক মডেল নাম: imagen-3.0-generate-001
            result = client.models.generate_images(
                model='imagen-3.0-generate-001',
                prompt=enhanced_prompt,
                config=types.GenerateImagesConfig(
                    number_of_images=1,
                    aspect_ratio="9:16",
                    output_mime_type="image/jpeg"
                )
            )
            
            for generated_image in result.generated_images:
                generated_image.image.save(img_path)
            
            print(f"✅ Scene {scene_num} generated with Imagen 3!")
            
            if scene_num < len(story_data['scenes']):
                time.sleep(5)
                
        except Exception as e:
            print(f"❌ Imagen API Error for Scene {scene_num}: {e}")
            images_success = False
            break

    return images_success
