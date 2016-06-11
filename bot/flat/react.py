# coding=utf-8
#
import telepot

from bot.flat.members import get_members
from bot.flat.api_actions import update_total

COMMAND_PUT = 'put'
COMMAND_LIST = 'list'
COMMAND_HELP = 'help'

ALLOWED_COMMANDS = [COMMAND_PUT, COMMAND_LIST, COMMAND_HELP]


def check_text_for_command_and_execute(home, message):
    content_type, chat_type, chat_id = telepot.glance(message)
    try:
        command_value = message["text"].split(" ")
        command = command_value[0].lower()
        if command not in ALLOWED_COMMANDS:
            raise Exception()
        if command == COMMAND_PUT:
            if len(command_value) != 2:
                home.bot.sendMessage(chat_id, "Missing the numeric value to add to your balance")
            value = float(command_value[1])
            update_total(home, value, chat_id)
            display_status(home, chat_id)
        if command == COMMAND_LIST:
            display_status(home, chat_id)
        if command == COMMAND_HELP:
            show_help_message(home, chat_id)
    except Exception as e:
        print(e)
        home.bot.sendMessage(chat_id, "Sorry, I could not understand your command")


def display_status(home, chat_id):
    member_list = get_members(home)
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
    home.bot.sendMessage(chat_id, response_text)


def show_help_message(home, chat_id):
    message = ("Available commands:\n\n\t\t1 - Put n: Adds n euros to your balance\n\t\t"
               "2 - List: Lists the balance for all the people in the flat")
    home.bot.sendMessage(chat_id, message)
