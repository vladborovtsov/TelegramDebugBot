#!/usr/bin/env python3.5
import telegram

import config as CONFIG

from flask import Flask, jsonify, abort, request
from telegram.bot import Bot
import chats_storage
import tempfile
import base64
import os


bot = Bot(CONFIG.TELEGRAM_BOT_TOKEN)

app = Flask(__name__)

@app.route('/')
def root():
    abort(404)

@app.route('/send-formatted', methods=['GET', 'POST'])
def send_formatted():
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


@app.route("/send-file", methods=['POST',])
def send_file():
    if request.json:
        try:
            text = request.json['text']
            secret = request.json["secret"]
            file_base64 = request.json["data"]
            file_ext = request.json["ext"]
        except KeyError as e:
            print(e)
            abort(400)

        if secret != CONFIG.REST_SECRET:
            abort(403)

        for cid in chats_storage.AllChatIds():
            f = tempfile.NamedTemporaryFile("w+b", suffix=".{}".format(file_ext))
            data = base64.decodebytes(file_base64.encode('utf8'))
            f.write(data)
            f.seek(0)

            bot.send_document(chat_id=cid, document=f, filename=os.path.basename(f.name), caption=text)

            f.close()


        return jsonify({"status" : "ok"})
    abort(400)

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=64501)