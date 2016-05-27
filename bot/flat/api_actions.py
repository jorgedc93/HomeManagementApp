#!/usr/bin/env python3.5
# coding=utf-8
#

import requests

from flat.config import procenca56


def update_total(home, amount, chat_id):
    url = home.endpoint + procenca56[chat_id] + "/"
    response = requests.get(url)
    user = response.json()['data']
    user["total"] += amount
    data = {"total": user["total"]}
    response = requests.put(url, json=data)
    if response.status_code != 200:
        home.bot.sendMessage(chat_id, "Uuuups, the server responded with :" + str(response.status_code))


def get_users_from_api_endpoint(home):
    response = requests.get(home.endpoint)
    return response.json()['data']

# def create_user(text):
#     try:
#         command, name = text.split()
#         if command == "make":
#             user = {
#                 "username": name,
#                 "total": 0,
#                 "_id": "571cbe0674fece454d648ab9"
#             }
#             response = requests.post(ENDPOINT, json=user)
#             print(response.status_code)
#     except ValueError:
#         print("text was not a valid command" + text)
