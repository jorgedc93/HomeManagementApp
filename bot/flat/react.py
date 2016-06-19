# coding=utf-8
#
import telepot

from bot.flat.members import get_members
from bot.flat.api_actions import update_total, create_new_flat

PUT = 'put'
LIST = 'list'
HELP = 'help'
NEW_FLAT = 'new_flat'
DELETE_FLAT = 'delete_flat'
JOIN = 'join'
LEAVE = 'leave'


ALLOWED_COMMANDS = [PUT, LIST, HELP, NEW_FLAT]


def check_text_for_command_and_execute(home_bot_cfg, message):
    content_type, chat_type, chat_id = telepot.glance(message)
    try:
        command_value = message["text"].split(" ")
        command = command_value[0].lower()
        print(command)
        del command_value[0]
        values = [argument for argument in command_value]
        if command not in ALLOWED_COMMANDS:
            raise Exception()
        if command == PUT:
            update_balance(home_bot_cfg, chat_id, values)
            display_status(home_bot_cfg, chat_id)
        elif command == LIST:
            display_status(home_bot_cfg, chat_id)
        elif command == HELP:
            show_help_message(home_bot_cfg, chat_id)
        elif command == NEW_FLAT:
            create_flat(home_bot_cfg, chat_id, values)
        elif command == DELETE_FLAT:
            print("dedwaewf")
            delete_flat(home_bot_cfg, chat_id)
        else:
            print("what")
    except Exception as e:
        print(e)
        home_bot_cfg.bot.sendMessage(chat_id, "Sorry, I could not understand your command")


def update_balance(home_bot_cfg, chat_id, value_list):
    if len(value_list) == 0:
        home_bot_cfg.bot.sendMessage(chat_id, "Missing the numeric value to add to your balance")
    value = float(value_list[0])
    update_total(home_bot_cfg, value, chat_id)


def display_status(home_bot_cfg, chat_id):
    member_list = get_members(home_bot_cfg)
    maximum_total_member = max(member_list, key=lambda x: x.get('total'))
    response = ["Balance :\n\n"]
    for member in member_list:
        if member == maximum_total_member:
            response.append(member["name"].capitalize() + ": " + str(round(member["total"], 2)) + "€ \n")
        else:
            difference_max = member["total"] - maximum_total_member["total"]
            response.append(member["name"].capitalize() + ": " + str(round(member["total"], 2)) + "€\t(" +
                            str(round(difference_max, 2)) + "€) \n")
    response_text = "".join(response)
    home_bot_cfg.bot.sendMessage(chat_id, response_text)


def show_help_message(home_bot_cfg, chat_id):
    message = ("Available commands:\n\n\t\t1 - Put n: Adds n euros to your balance\n\t\t"
               "2 - List: Lists the balance for all the people in the flat")
    home_bot_cfg.bot.sendMessage(chat_id, message)


def create_flat(home_bot_cfg, chat_id, value_list):
    if len(value_list) != 2:
        home_bot_cfg.bot.sendMessage("To create a flat use it like the following:\n\t\t 'flat name_of_flat password'")
    else:
        create_new_flat(home_bot_cfg, chat_id, value_list)


def delete_flat(home_bot_cfg, chat_id):
    pass
