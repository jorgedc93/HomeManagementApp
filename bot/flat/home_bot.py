#!/usr/bin/env python3.5
# coding=utf-8
#

import telepot

from flat.config import bot_cfg

ENDPOINT = "http://192.168.1.232:5000/api/v1/users/"


class HomeBot(object):

    def __init__(self):
        self.bot = telepot.Bot(bot_cfg["token"])
        self.endpoint = ENDPOINT
