#!/usr/bin/env python3.5
import telegram

import config as CONFIG

from flask import Flask, jsonify, abort, request
from telegram.bot import Bot
import chats_storage


bot = Bot(CONFIG.TELEGRAM_BOT_TOKEN)

app = Flask(__name__)

@app.route('/')
def root():
    abort(404)

@app.route('/send-formatted', methods=['GET', 'POST'])
def send_formatted():
    print(request.values)
    if request.json:
        try:
            caption = request.json["caption"]
            text = request.json['text']
            secret = request.json["secret"]
        except KeyError as e:
            print(e)
            abort(400)

        if secret != CONFIG.REST_SECRET:
            abort(403)

        for cid in chats_storage.AllChatIds():
            bot.send_message(cid, parse_mode=telegram.ParseMode.HTML, text="<b>{}</b>\n<pre>{}</pre>".format(caption,text))
        return jsonify({"status" : "ok"})
    abort(400)

if __name__ == '__main__':
    app.run(debug=True)