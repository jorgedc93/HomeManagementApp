#!/usr/bin/env python3.5
# coding=utf-8
#
import telepot

from flat.members import get_members
from flat.api_actions import update_total


def check_text_for_command_and_execute(home, message):
    content_type, chat_type, chat_id = telepot.glance(message)
    try:
        command_value = message["text"].split(" ")
        if len(command_value) != 2:
            raise()
        if command_value[0].lower() != 'put':
            raise()
        if isinstance(command_value[1], str):
            value = int(command_value[1])

            if isinstance(value, int):
                update_total(home, value, chat_id)
            else:
                raise()
    except:
        home.bot.sendMessage(chat_id, "I am a very simple bot at the Moment. Please write 'put 5' if you want to add 5 euros")


def display_status(home, chat_id):
    member_list = get_members(home)
    response = "Balance :\n"
    for member in member_list:
        response += member["name"] + " :" + str(member["total"]) + "\n"
    home.bot.sendMessage(chat_id, response)
