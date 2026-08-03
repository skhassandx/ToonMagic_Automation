import os
import time
from playwright.sync_api import sync_playwright
from config.settings import IMAGES_DIR

def generate_images_via_browser(prompt, scene_num):
    username = os.environ.get("LEONARDO_USER")
    password = os.environ.get("LEONARDO_PASS")

    with sync_playwright() as p:
        # ব্রাউজার ওপেন করা (গিটহাবে headless=True রাখতে হবে)
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64)..."
        )
        page = context.new_page()

        try:
            print("🌐 Opening Leonardo.ai...")
            page.goto("https://app.leonardo.ai/auth/login")
            time.sleep(5)

            # লগইন ক্রেডেনশিয়াল দেওয়া (যদি Cloudflare ব্লক না করে)
            page.fill('input[type="email"]', username)
            page.fill('input[type="password"]', password)
            page.click('button[type="submit"]')
            print("✅ Logged in successfully!")
            time.sleep(10)

            # ইমেজ জেনারেশন পেজে যাওয়া এবং প্রম্পট দেওয়া
            page.goto("https://app.leonardo.ai/image-generation")
            time.sleep(5)
            page.fill('textarea[placeholder="Type a prompt..."]', prompt)
            page.click('button:has-text("Generate")')
            
            print("⏳ Waiting for image generation...")
            time.sleep(20) # ছবি তৈরি হওয়ার সময়

            # ছবি ডাউনলোড করার লজিক...
            # (এখানে DOM থেকে ইমেজের URL বের করে ডাউনলোড করতে হবে)
            
        except Exception as e:
            print(f"⚠️ Browser Automation Failed: {e}")
        finally:
            browser.close()
