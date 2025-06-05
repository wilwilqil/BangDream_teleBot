import os
import telebot
import requests
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()
BOT_TOKEN = os.environ.get('BOT_TOKEN')
if not BOT_TOKEN:                                           # Verify token is loaded
    raise ValueError("BOT_TOKEN not found in .env file")
bot = telebot.TeleBot(BOT_TOKEN)

#command list
@bot.message_handler(commands=
                     ['start', 'hello', 'hi', 
                      '你好', '你', '妳', '他', '它'])
def send_welcome(message):
    bot.reply_to(message, "要跟我組一輩子的樂團嗎")

@bot.message_handler(func=lambda message: True)
def echo_all(message):
	bot.reply_to(message, message.text)

if __name__ == "__main__":
    print("Bot is starting...")
    try:
        bot.infinity_polling()
    except Exception as e:
        print(f"Bot failed to start: {str(e)}")