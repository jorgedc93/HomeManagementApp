# coding=utf-8
#

import telepot

from flat.config import bot_cfg


class HomeBot(object):

    def __init__(self):
        self.bot = telepot.Bot(bot_cfg["token"])
