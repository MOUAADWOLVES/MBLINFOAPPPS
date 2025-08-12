import requests
import json
import time

TOKEN = "5587533183:AAGJSv4NFux5yvHOa8g2QVE2cs4tZjKNCVY"
API_URL = "https://magicphotos.com/api/generate-art"
LAST_UPDATE_ID = 0

def get_updates():
    global LAST_UPDATE_ID
    url = f"https://api.telegram.org/bot{TOKEN}/getUpdates?offset={LAST_UPDATE_ID + 1}"
    response = requests.get(url)
    return response.json().get("result", [])

def send_message(chat_id, text):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    data = {"chat_id": chat_id, "text": text}
    requests.post(url, json=data)

def send_photo(chat_id, photo_bytes, caption=""):
    url = f"https://api.telegram.org/bot{TOKEN}/sendPhoto"
    files = {"photo": ("image.png", photo_bytes)}
    data = {"chat_id": chat_id, "caption": caption}
    requests.post(url, files=files, data=data)

def generate_image(prompt):
    try:
        response = requests.post(
            API_URL,
            json={"prompt": prompt, "userProfile": {}},
            headers={"Content-Type": "application/json"},
            timeout=30
        )
        return response.content
    except Exception as e:
        print(f"Error: {e}")
        return None

def handle_updates():
    global LAST_UPDATE_ID
    while True:
        updates = get_updates()
        for update in updates:
            LAST_UPDATE_ID = update["update_id"]
            
            if "message" in update:
                message = update["message"]
                chat_id = message["chat"]["id"]
                text = message.get("text", "")
                
                if text.startswith("/start"):
                    send_message(chat_id, "مرحباً! أنا بوت توليد الصور. أرسل /image ووصف الصورة")
                
                elif text.startswith("/image"):
                    prompt = text[6:].strip()
                    if prompt:
                        send_message(chat_id, "⏳ جاري توليد الصورة...")
                        image_data = generate_image(prompt)
                        if image_data:
                            send_photo(chat_id, image_data, f"الصورة المطلوبة: {prompt}")
                        else:
                            send_message(chat_id, "❌ فشل في توليد الصورة")
                    else:
                        send_message(chat_id, "الرجاء إدخال وصف للصورة بعد الأمر /image")
        
        time.sleep(1)

if __name__ == "__main__":
    print("Bot is running...")
    handle_updates()