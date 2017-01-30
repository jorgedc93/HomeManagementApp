# coding=utf-8
#

import requests

from flat.config import provenca56

ENDPOINT = "http://localhost:5000/api/v1/users/"

session = requests.Session()


def update_total(home, amount, chat_id):
    url = ENDPOINT + provenca56[chat_id] + "/"
    response = session.get(url)
    user = response.json()['data']
    user["total"] += amount
    data = {"total": user["total"]}
    response = session.put(url, json=data)
    if response.status_code != 200:
        home.bot.sendMessage(chat_id, "Uuuups, the server responded with :" + str(response.status_code))


def get_users_from_api_endpoint(home):
    response = session.get(home.endpoint)
    return response.json()['data']
