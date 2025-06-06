import os
import telebot
import requests
from dotenv import load_dotenv

class TelegramBot:
    def __init__(self):
        # Load environment variables from .env file
        load_dotenv()
        self.bot_token = os.environ.get('BOT_TOKEN')
        if not self.bot_token: raise ValueError("BOT_TOKEN not found in .env file")
        self.bot = telebot.TeleBot(self.bot_token)
        self.register_handlers()

    def register_handlers(self):
        """Register all message handlers for the bot."""
        @self.bot.message_handler(commands=[
            'start', 'hello', 'hi',
            '你好', '你', '妳', '他', '它'])
        def send_welcome(message):
            self.bot.reply_to(message, "要跟我組一輩子的樂團嗎")

        @self.bot.message_handler(func=lambda message: True)
        def echo_all(message):
            self.bot.reply_to(message, message.text)

    def start(self):
        """Start the bot with infinity polling."""
        print("Bot is starting...")
        try:
            self.bot.infinity_polling()
        except Exception as e:
            print(f"Bot failed to start: {str(e)}")

if __name__ == "__main__":
    bot_instance = TelegramBot()
    bot_instance.start()