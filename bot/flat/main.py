#!/usr/bin/env python3.5
# coding=utf-8
#

import telepot
import time
import requests
import json

from  flat.members import Member
from flat.config import bot_cfg, procenca56

ENDPOINT = "http://192.168.1.232:5000/api/v1/users/"

def run():
    bot = telepot.Bot(bot_cfg["token"])
    bot.message_loop(react_on_message)
    print("Bot is running...")


def react_on_message(message):
    content_type, chat_type, chat_id = telepot.glance(message)
    if not_authorised(content_type, chat_id):
        if put_money(message["text"]):
            print(message["text"])
            _ , amount = message["text"].split(" ")
            print(_)
            print()
            print(amount)
            print()
            amount = int(amount)
            update_total(amount, chat_id)
        member_list = get_members()
        telepot.Bot(bot_cfg["token"]).sendMessage(chat_id, str(member_list))


def not_authorised(content_type, chat_id):
        return content_type == "text" and chat_id in procenca56.keys()


def get_members():
    user_list = get_users_from_api_endpoint()
    return [Member(user["username"], user["total"]).to_dict() for user in user_list]


def get_users_from_api_endpoint():
    response = requests.get(ENDPOINT)
    return response.json()['data']


def update_total(amount, chat_id):
    url = ENDPOINT + procenca56[chat_id] + "/"
    response = requests.get(url)
    user = response.json()['data']
    print()
    print(str(user))
    print()
    user["total"] += amount
    print()
    print(str(user))
    print()
    data = {"total": user["total"]}
    response = requests.put(url, data=json.dumps(data))
    print()
    print(str(response))
    print()


def put_money(text):
    command, amount = text.split()
    return command == "put"


if __name__ == '__main__':
    run()
    # Keep the program running.
    while 1:
        time.sleep(10)


def get_usernames():
    user_dict =  get_users_from_api_endpoint()
    return list_of("username", user_dict)


def get_users_total():
    user_dict = get_users_from_api_endpoint()
    return list_of("total", user_dict)


def list_of(key, dict):
    return [user[key] for user in dict]
