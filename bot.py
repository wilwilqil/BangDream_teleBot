import os
import telebot
from flask import Flask, request
from dotenv import load_dotenv

app = Flask(__name__)

# Load environment variables
load_dotenv()
BOT_TOKEN = os.environ.get('BOT_TOKEN')
if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN not found in .env file")
bot = telebot.TeleBot(BOT_TOKEN)

# Register handlers
@bot.message_handler(commands=['start', 'hello', 'hi', '你好', '你', '妳', '他', '它'])
def send_welcome(message):
    bot.reply_to(message, "要跟我組一輩子的樂團嗎")

@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.reply_to(message, message.text)

# Webhook route
@app.route('/' + BOT_TOKEN, methods=['POST'])
def get_message():
    json_str = request.get_data().decode('UTF-8')
    update = telebot.types.Update.de_json(json_str)
    bot.process_new_updates([update])
    return '!', 200

@app.route('/')
def webhook():
    bot.remove_webhook()
    bot.set_webhook(url=f'https://<your-app-name>.azurewebsites.net/{BOT_TOKEN}')
    return 'Webhook set', 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))