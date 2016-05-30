# coding=utf-8
#
import telepot

from bot.flat.members import get_members
from bot.flat.api_actions import update_total

COMMAND_PUT = 'put'
COMMAND_LIST = 'list'

ALLOWED_COMMANDS = [COMMAND_PUT, COMMAND_LIST]


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
    except:
        home.bot.sendMessage(chat_id, "I am a very simple bot at the Moment. Please write 'put 5' if you "
                                      "want to add 5 euros")


def display_status(home, chat_id):
    member_list = get_members(home)
    response = ["Balance :\n\n"]
    for member in member_list:
        response.append(member["name"].capitalize() + ": " + str(round(member["total"], 2)) + "€ \n")
    response_text = "".join(response)
    home.bot.sendMessage(chat_id, response_text)
