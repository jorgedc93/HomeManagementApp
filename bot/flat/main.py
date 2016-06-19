#!/usr/bin/env python3.5
# coding=utf-8
#

import telepot
import time

from bot.flat.home_bot import HomeBot
from bot.flat.config import provenca56
from bot.flat.react import check_text_for_command_and_execute


def authorised(content_type, chat_id):
        return content_type == "text" and chat_id in provenca56.keys()


def run():
    home_bot_cfg = HomeBot()
    home_bot_cfg.bot.message_loop(react_on_message)
    print("Bot is running...")


def react_on_message(message):
    home_bot_cfg = HomeBot()
    content_type, chat_type, chat_id = telepot.glance(message)
    if authorised(content_type, chat_id):
        check_text_for_command_and_execute(home_bot_cfg, message)
        pass

if __name__ == '__main__':
    run()
    # Keep the program running.
    while 1:
        time.sleep(10)
