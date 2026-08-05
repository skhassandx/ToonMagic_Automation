import os
import json
import time
import requests
from io import BytesIO
from PIL import Image, ImageFilter
from config.settings import IMAGES_DIR

def generate_images(story_path):
    print("🎨 Generating Images using Cloudflare Workers AI (Super Fast & Stable)...")
    
    with open(story_path, 'r', encoding='utf-8') as f:
        story_data = json.load(f)

    # Cloudflare Credentials
    account_id = os.environ.get("CLOUDFLARE_ACCOUNT_ID")
    api_token = os.environ.get("CLOUDFLARE_API_TOKEN")

    if not account_id or not api_token:
        print("❌ CRITICAL ERROR: Cloudflare credentials (Account ID or Token) not found in GitHub Secrets!")
        return False

    images_success = True
    
    # Cloudflare এর লেটেস্ট Stable Diffusion XL মডেল
    model = "@cf/stabilityai/stable-diffusion-xl-base-1.0"
    url = f"https://api.cloudflare.com/client/v4/accounts/{account_id}/ai/run/{model}"
    headers = {"Authorization": f"Bearer {api_token}"}

    for scene in story_data['scenes']:
        scene_num = scene['scene_number']
        img_path = os.path.join(IMAGES_DIR, f"scene_{scene_num}.jpg")

        # স্কিপ লজিক (আগের ছবি থাকলে নতুন করে বানাবে না)
        if os.path.exists(img_path):
            print(f"⏭️ Scene {scene_num} already exists. Skipping...")
            continue

        raw_prompt = scene.get('image_prompt', "A cute cartoon character")
        enhanced_prompt = f"3D Pixar style, masterpiece, highly detailed, vibrant colors, {raw_prompt}, wide angle shot, full body"
        
        image_downloaded = False
        
        for attempt in range(3):
            try:
                print(f"🔄 Trying Cloudflare AI for Scene {scene_num}...")
                
                # Cloudflare API তে রিকোয়েস্ট পাঠানো
                response = requests.post(url, headers=headers, json={"prompt": enhanced_prompt}, timeout=60)
                
                if response.status_code == 200:
                    original_img = Image.open(BytesIO(response.content)).convert("RGB")
                    
                    target_width, target_height = 1080, 1920
                    
                    # সিনেমাটিক ব্লার প্যাডিং
                    fg_img = original_img.resize((1080, 1080))
                    bg_img = original_img.resize((target_width, target_height))
                    bg_img = bg_img.filter(ImageFilter.GaussianBlur(radius=35))
                    
                    y_offset = (target_height - 1080) // 2
                    bg_img.paste(fg_img, (0, y_offset))
                    
                    bg_img.save(img_path, "JPEG", quality=95)
                    
                    print(f"✅ Scene {scene_num} image saved successfully!")
                    image_downloaded = True
                    break 
                else:
                    print(f"⚠️ Cloudflare Error {response.status_code}: {response.text}")
                    time.sleep(5)
                    
            except Exception as e:
                print(f"⚠️ Request failed: {e}. Retrying...")
                time.sleep(5)
                
        if not image_downloaded:
            print(f"❌ CRITICAL ERROR: Failed to generate image for Scene {scene_num}")
            images_success = False
            break

    return images_success
