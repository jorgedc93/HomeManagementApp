# coding=utf-8

import requests

from bot.flat.config import provenca56


def update_total(home_bot_cfg, amount, chat_id):
    chat_id = str(provenca56[chat_id])
    user = get_single_user_from_api_endpoint(home_bot_cfg, chat_id)
    user["total"] += amount
    response = put_users_total_amount_to_api_endpoint(home_bot_cfg, chat_id, user["total"])
    if response.status_code != 200:
        home_bot_cfg.bot.sendMessage(chat_id, "Uuuups, the server responded with :" + str(response.status_code))


def get_all_users_from_api_endpoint(home_bot_cfg):
    response = requests.get(home_bot_cfg.endpoint + 'users/')
    return response.json()['data']


def get_single_user_from_api_endpoint(home_bot_cfg, chat_id):
    url = home_bot_cfg.endpoint + 'users/' + chat_id + "/"
    response = requests.get(url)
    if response.status_code != 200:
        raise UserNotFoundException('USER_NOT_FOUND', 'Could not load user with id {} from API'.format(chat_id))
    return response.json()['data']


def put_users_total_amount_to_api_endpoint(home_bot_cfg, chat_id, new_total):
    url = home_bot_cfg.endpoint  + 'users/' + chat_id + "/"
    data = {"total": new_total}
    return requests.put(url, json=data)


def create_new_flat(home_bot_cfg, chat_id, value_list):
    user = get_single_user_from_api_endpoint(home_bot_cfg, chat_id)
    if user["flat"] != 'None':
        flat = {
            "flatname": value_list[0],
            "flat_members": [chat_id],
            "shopping_list": ["beer"],
            "password": value_list[1],
            "admin": chat_id
        }
        requests.post(home_bot_cfg.endpoint + 'flats/', json=flat)
    else:
        home_bot_cfg.bot.sendMessage(chat_id, "You already have a flat")



class UserNotFoundException(Exception):
    def __init__(self, error, message=""):
        self.error = error
        self.message = message
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
