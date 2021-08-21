import json
import logging
import os

import telebot
# from telebot import apihelper
from flask import Flask, request

import constants as C


TOKEN = os.environ.get("TG_API_TOKEN", None)
if TOKEN is None:
    with open("tg_token.txt") as fin:
        TOKEN = fin.readline().replace("\n", "")

WEBHOOK_URI = getattr(C, "WEBHOOK_URI", None)
DEBUG = os.environ.get("DEBUG", False)

if WEBHOOK_URI is None and not DEBUG:
    vcap_application = json.loads(os.environ["VCAP_APPLICATION"])
    WEBHOOK_URI = vcap_application["uris"][0]


log = telebot.logger
server = Flask(__name__)
# apihelper.proxy = {"https": C.PROXY, "http": C.PROXY}
bot = telebot.TeleBot(TOKEN)

if DEBUG:
    telebot.logger.setLevel(logging.DEBUG)

log.info(bot.get_me())


@bot.message_handler(commands=["help", "start"])
def send_welcome(message):
    bot.reply_to(message, C.MSG_GREETING)


@bot.message_handler(func=lambda message: True)
def echo_message(message):
    bot.reply_to(message, message.text)


@server.route("/" + TOKEN, methods=["POST"])
def getMessage():
    bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
    return "!", 200


@server.route("/")
def webhook():
    bot.remove_webhook()
    bot.set_webhook(url=f"https://{WEBHOOK_URI}/{TOKEN}")
    return "!", 200


if __name__ == "__main__":
    if not DEBUG:
        server.run(host=C.HOST, port=int(os.environ.get("PORT", C.PORT)))

    else:
        bot.polling()
