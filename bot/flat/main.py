#!/usr/bin/env python3.5
# coding=utf-8
#

import telepot
import time

from flat.config import bot_cfg, procenca56


def run():
    bot = telepot.Bot(bot_cfg["token"])
    bot.message_loop(react_on_message)
    print("Bot is running...")


def react_on_message(message):
    content_type, chat_type, chat_id = telepot.glance(message)
    if not_authorised(content_type, chat_id):
        text = message["text"]
        telepot.Bot(bot_cfg["token"]).sendMessage(chat_id, "What do you mean with " + text + " ?")
        

def not_authorised(content_type, chat_id):
        return content_type == "text" and chat_id in procenca56.keys()


if __name__ == '__main__':
    run()
    # Keep the program running.
    while 1:
        time.sleep(10)
