import os
import random
import threading
import time
from flask import Flask
from instagrapi import Client

# Render o'chirib qo'ymasligi uchun kichik veb-server
app = Flask(__name__)


@app.route("/")
def home():
  return "Instagram Follow Bot ishlamoqda! 🍃"


# --- SOZLAMALAR ---
SESSION_ID = (
    "44907967558%3AbPxtoXXLbExel9%3A26%3AAYnvJTjDW4c3-xkqTyZOTbBDAZTuHD3v4_VlXhSHnA"
)
DAILY_LIMIT = 120
TARGET_USERNAME = "umr.sham"  # Kimning obunachilariga obuna bo'lish kerakligi


def run_bot():
  print("Bot ishga tushdi, Instagram bilan bog'lanilmoqda...")
  cl = Client()
  try:
    cl.login_by_sessionid(SESSION_ID)
    print("Muvaffaqiyatli session orqali kirildi!")
  except Exception as e:
    print(f"Session xatosi: {e}")
    return

  print(f"\n[{TARGET_USERNAME}] ning obunachilari olinmoqda...")
  try:
    target_user_id = cl.user_id_from_username(TARGET_USERNAME)
    followers = cl.user_followers(target_user_id, amount=DAILY_LIMIT)
  except Exception as e:
    print(f"Obunachilarni olishda xatolik: {e}")
    return

  print(f"Topildi: {len(followers)} ta odam. Jarayon boshlandi...")
  followed_count = 0

  for user_id, user_info in followers.items():
    if followed_count >= DAILY_LIMIT:
      print("Kunlik limit (120 ta) tugadi. Bot to'xtatildi.")
      break

    username = user_info.username
    try:
      # 1. Obuna bo'lish
      cl.user_follow(user_id)
      followed_count += 1
      print(f"[{followed_count}/{DAILY_LIMIT}] @{username} ga obuna bo'lindi.")

      # 2. 10 soniya kutib lichkaga yozish
      print("10 soniya kutilmoqda va lichkaga yozilmoqda...")
      time.sleep(10)

      try:
        cl.direct_send("folow qaytaring 🍃", [user_id])
        print(f"@{username} ga xabar yuborildi.")
      except Exception as msg_err:
        print(f"Xabar yuborib bo'lmadi: {msg_err}")

      # 3. 40 soniya atrofida pauza (bloklanmaslik uchun)
      sleep_time = random.randint(38, 45)
      print(f"Xavfsizlik uchun {sleep_time} soniya kutilmoqda...\n")
      time.sleep(sleep_time)

    except Exception as e:
      print(f"Xatolik (@{username}): {e}")
      time.sleep(15)

  print("\nBarcha vazifalar bajarildi!")


# Asosiy qism
if __name__ == "__main__":
  # Botni alohida oqimda (background'da) ishga tushiramiz
  bot_thread = threading.Thread(target=run_bot)
  bot_thread.daemon = True
  bot_thread.start()

  # Render beradigan portda Flask serverni yoqamiz
  port = int(os.environ.get("PORT", 10000))
  app.run(host="0.0.0.0", port=port)
  
