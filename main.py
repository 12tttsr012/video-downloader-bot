import os
import telebot
import yt_dlp
from flask import Flask
from threading import Thread

# جلب التوكن من إعدادات رندر
TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is Running!"

def run_web_server():
    # تشغيل سيرفر ويب بسيط لإبقاء البوت مستيقظاً
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))

@bot.message_handler(func=lambda message: True)
def download_video(message):
    url = message.text
    if not url.startswith("http"):
        bot.reply_to(message, "⚠️ أرسل رابطاً صالحاً من فضلك.")
        return

    bot.reply_to(message, "⏳ جاري التحميل... انتظر قليلاً")
    
    ydl_opts = {
        'format': 'best',
        'outtmpl': 'video.mp4',
        'max_filesize': 45000000, # الحد الأقصى 45 ميجا
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        
        with open('video.mp4', 'rb') as video:
            bot.send_video(message.chat.id, video)
        os.remove('video.mp4') # حذف الملف لتوفير المساحة
    except Exception as e:
        bot.reply_to(message, f"❌ خطأ: الرابط غير مدعوم أو حجمه كبير")

if __name__ == "__main__":
    Thread(target=run_web_server).start()
    bot.infinity_polling()
