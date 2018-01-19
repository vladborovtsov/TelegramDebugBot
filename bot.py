#!/usr/bin/env python3.5
from threading import Thread

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import logging
import config as CONFIG
import json
import os


if os.path.exists(CONFIG.CHAT_IDs_FILENAME):
    CHATS = json.load(open(CONFIG.CHAT_IDs_FILENAME, "r+t"))
else:
    CHATS = []

def save_chats():
    f = open(CONFIG.CHAT_IDs_FILENAME, "w+t")
    f.write(json.dumps(CHATS, indent=1))
    f.close()

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


# Define a few command handlers. These usually take the two arguments bot and
# update. Error handlers also receive the raised TelegramError object in error.
def start(bot, update):
    """Send a message when the command /start is issued."""
    update.message.reply_text('Hi!')


def help(bot, update):
    """Send a message when the command /help is issued."""
    update.message.reply_text('Available commands: \n/on <SECRET> \n/off')


def echo(bot, update):
    """Echo the user message."""
    update.message.reply_text(update.message.text)

def on(bot, update):
    logger.log(logging.INFO, update.message.text)
    auth = update.message.text.split(" ")
    if auth[1] == CONFIG.SECRET:
        for chat in CHATS:
            if update.message.chat.id == chat["id"]:
                update.message.reply_text("You are subscribed already!");
                return
        update.message.reply_text("Subscribed.")
        CHATS.append(json.loads(update.message.chat.to_json()))
        save_chats()
    else:
        update.message.reply_text("Wrong secret.")


def off(bot,update):
    for chat in CHATS:
        if update.message.chat.id == chat["id"]:
            CHATS.remove(chat)
            update.message.reply_text("You have been successfully unsubcribed!");
            save_chats()
            return

    update.message.reply_text("User not found.");


def error(bot, update, error):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, error)


def main():
    """Start the bot."""
    # Create the EventHandler and pass it your bot's token.
    updater = Updater(CONFIG.TELEGRAM_BOT_TOKEN)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("on", on))
    dp.add_handler(CommandHandler("off", off))

    # on noncommand i.e message - echo the message on Telegram
    dp.add_handler(MessageHandler(Filters.text, echo))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()


    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()



class Api(Thread):
    def run(self):
        from flask_api import FlaskAPI
        app = FlaskAPI(__name__)
        app.run(debug=False)


if __name__ == '__main__':
    print("Starting api...")
    api = Api()
    api.start()
    print("Starting bot...")
    main()
    save_chats()

