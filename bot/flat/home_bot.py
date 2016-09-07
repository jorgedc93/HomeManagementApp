# coding=utf-8
#

import telepot

from bot.flat.config import bot_cfg

ENDPOINT = "http://localhost:5000/api/v1/users/"


class HomeBot(object):

    def __init__(self):
        self.bot = telepot.Bot(bot_cfg["token"])
        self.endpoint = ENDPOINT
