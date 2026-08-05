import os
import json
import time
from io import BytesIO
from PIL import Image, ImageFilter
from huggingface_hub import InferenceClient
from config.settings import IMAGES_DIR

def generate_images(story_path):
    print("🎨 Generating Images using Hugging Face (Ungated Open Models)...")
    
    with open(story_path, 'r', encoding='utf-8') as f:
        story_data = json.load(f)

    api_key = os.environ.get("HF_API_KEY")
    if not api_key:
        print("❌ CRITICAL ERROR: HF_API_KEY not found!")
        return False

    client = InferenceClient(token=api_key)
    images_success = True

    # 🌟 ১০০% ওপেন এবং ফ্রি মডেলের তালিকা (কোনো Gated বা লাইসেন্স এগ্রিমেন্টের ঝামেলা নেই)
    open_models = [
        "prompthero/openjourney",             # কার্টুন ও আর্টের জন্য সেরা
        "cagliostrolab/animagine-xl-3.1",     # হাই-কোয়ালিটি অ্যানিমেশন
        "black-forest-labs/FLUX.1-schnell"    # লেটেস্ট ফাস্ট জেনারেশন মডেল
    ]

    for scene in story_data['scenes']:
        scene_num = scene['scene_number']
        img_path = os.path.join(IMAGES_DIR, f"scene_{scene_num}.jpg")

        if os.path.exists(img_path):
            continue

        prompt = scene.get('image_prompt', "A cute cartoon character")
        enhanced_prompt = f"3D Pixar style, masterpiece, highly detailed, vibrant colors, {prompt}, wide angle shot, full body"
        
        image_downloaded = False
        
        for attempt in range(3):
            for model_name in open_models:
                try:
                    print(f"🔄 Trying open model: {model_name} for Scene {scene_num}...")
                    
                    image = client.text_to_image(
                        enhanced_prompt,
                        model=model_name
                    )
                    
                    # 🌟 সিনেমাটিক ব্লার প্যাডিং
                    original_img = image.convert("RGB")
                    target_width, target_height = 1080, 1920
                    
                    fg_img = original_img.resize((1080, 1080))
                    bg_img = original_img.resize((target_width, target_height))
                    bg_img = bg_img.filter(ImageFilter.GaussianBlur(radius=35))
                    
                    y_offset = (target_height - 1080) // 2
                    bg_img.paste(fg_img, (0, y_offset))
                    
                    bg_img.save(img_path, "JPEG", quality=95)
                    
                    print(f"✅ Scene {scene_num} image saved successfully!")
                    image_downloaded = True
                    break # সফল হলে মডেল লুপ ভাঙবে
                    
                except Exception as e:
                    print(f"⚠️ {model_name} failed: {e}")
                    print("⏳ Trying next open model...")
                    time.sleep(3)
                    
            if image_downloaded:
                break # সফল হলে attempt লুপ ভাঙবে
            else:
                print("⏳ All models failed for this attempt. Waiting 10s before retry...")
                time.sleep(10)

        if not image_downloaded:
            print(f"❌ CRITICAL ERROR: Failed to generate image for Scene {scene_num}")
            images_success = False
            break

    return images_success
