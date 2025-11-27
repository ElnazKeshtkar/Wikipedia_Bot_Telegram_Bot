import os
from dotenv import load_dotenv
import telebot
import wikipedia

load_dotenv()

API_KEY = os.getenv("MY_TOKEN")

if not API_KEY:
    print("Error: Token not found! Did you create the .env file?")
else:
    print("Token found! Starting bot...")

# Connect to your bot
bot = telebot.TeleBot(API_KEY)

# Set the language to English
wikipedia.set_lang("fa")

# 1. Start Command
@bot.message_handler(commands=["start"])
def welcome(message):
    bot.send_message(message.chat.id, "سلام خوش آمدید! هر کلمه‌ای که تایپ کنی من برایت معنی آن را در ویکی پدیا پیدا می کنم.")

# 2. Help Command
@bot.message_handler(commands=["help"])
def help_command(message):
    help_text = "Here are availble commands: \n/start-Start the bot\n/help-Get help"
    bot.send_message(message.chat.id, help_text)

# 3. The Wiki Handler
@bot.message_handler(func=lambda message : True)
def get_wiki(message):    
    bot.reply_to(message, "درحال جستجو ...")

    try:
        topic = message.text
        page = wikipedia.page(topic)
        title = page.title
        summary = wikipedia.summary(topic, sentences=3)
        response = f"{title}\n\n{summary}"
        bot.send_message(message.chat.id, response, parse_mode="Markdown")
    
    except wikipedia.exceptions.DisambiguationError as error:
        bot.send_message(message.chat.id, "این کلمه معانی مختلفی دارد. لطفاً دقیق‌تر بگویید.")
    
    except wikipedia.exceptions.PageError as error:
        bot.send_message(message.chat.id, "متاسفانه صفحه‌ای برای این موضوع پیدا نشد.")

    except Exception as error:
        bot.send_message(message.chat.id, "مشکلی پیش آمده،لطفا دوباره تلاش کنید.")

print("Wikipedia is running ...")
bot.polling(non_stop=True)
