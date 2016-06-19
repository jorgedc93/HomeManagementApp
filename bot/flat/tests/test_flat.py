# -*- coding: utf-8 -*-

import unittest
import requests
from unittest.mock import patch

from bot.flat.react import check_text_for_command_and_execute, create_flat
from bot.flat.home_bot import HomeBot
from bot.flat.tests.utils import generate_message, generate_random_user
from bot.flat.api_actions import create_new_flat


class FlatTestCase(unittest.TestCase):

    @patch("bot.flat.react.create_flat")
    def test_create_flat(self, create_flat_mock):
        home_bot_cfg = HomeBot()
        message = generate_message("new_flat provenca password")
        chat_id = message['chat']['id']
        with patch.object(home_bot_cfg.bot, 'sendMessage'):
            check_text_for_command_and_execute(home_bot_cfg, message)

        create_flat_mock.assert_called_once_with(home_bot_cfg, chat_id, ['provenca', 'password'])

    @patch("bot.flat.react.create_flat")
    def test_create_flat_only_if_begins_with_flat(self, create_flat_mock):
        home_bot_cfg = HomeBot()
        message = generate_message("flut provenca password")
        with patch.object(home_bot_cfg.bot, 'sendMessage'):
            check_text_for_command_and_execute(home_bot_cfg, message)

        create_flat_mock.assert_not_called()

    @patch("bot.flat.react.create_new_flat")
    def test_create_new_flat_(self, create_new_mock):
        home_bot_cfg = HomeBot()
        with patch.object(home_bot_cfg.bot, 'sendMessage') as send_mock:
            create_flat(home_bot_cfg, '12345678', ['one', 'two'])

        create_new_mock.assert_called_once_with(home_bot_cfg, '12345678', ['one', 'two'])
        send_mock.assert_not_called()

    @patch("bot.flat.react.create_new_flat")
    def test_create_new_flat_not_with_1_argument(self, create_new_mock):
        home_bot_cfg = HomeBot()
        with patch.object(home_bot_cfg.bot, 'sendMessage') as send_mock:
            create_flat(home_bot_cfg, '12345678', ['one'])

        create_new_mock.assert_not_called()
        send_mock.assert_called_once_with("To create a flat use it like the following:\n\t\t "
                                          "'flat name_of_flat password'")

    @patch("bot.flat.react.create_new_flat")
    def test_create_new_flat_not_with_3_arguments(self, create_new_mock):
        home_bot_cfg = HomeBot()
        with patch.object(home_bot_cfg.bot, 'sendMessage') as send_mock:
            create_flat(home_bot_cfg, '12345678', ['one', 'two', 'three'])

        create_new_mock.assert_not_called()
        send_mock.assert_called_once_with("To create a flat use it like the following:\n\t\t "
                                          "'flat name_of_flat password'")

    @patch("bot.flat.api_actions.get_single_user_from_api_endpoint")
    def test_before_creating_flat_get_user_endpoint_called(self, get_user_mock):
        home_bot_cfg = HomeBot()
        create_new_flat(home_bot_cfg, '12345678', ['flat_name', 'itsapassword'])

        get_user_mock.assert_called_once_with(home_bot_cfg, '12345678')

    @patch("bot.flat.api_actions.get_single_user_from_api_endpoint")
    def test_user_has_flat_no_create_happens(self, get_user_mock):
        user_no_flat = generate_random_user()
        user_no_flat["flat"] = "None"
        get_user_mock.return_value = user_no_flat
        home_bot_cfg = HomeBot()
        with patch.object(requests, 'post') as post_mock:
            with patch.object(home_bot_cfg.bot, 'sendMessage'):
                create_new_flat(home_bot_cfg, '12345678', ['flat_name', 'itsapassword'])

        post_mock.assert_not_called()

    @patch("bot.flat.api_actions.requests.post")
    @patch("bot.flat.api_actions.get_single_user_from_api_endpoint")
    def test_user_has_no_flat_create_happens(self, get_user_mock, post_mock):
        user_no_flat = generate_random_user()
        get_user_mock.return_value = user_no_flat
        home_bot_cfg = HomeBot()

        create_new_flat(home_bot_cfg, '12345678', ['flat_name', 'itsapassword'])

        post_mock.assert_called_once_with(home_bot_cfg.endpoint + 'flats/', json={'shopping_list': ['beer'],
                                                                                  'flat_members': ['12345678'],
                                                                                  'password': 'itsapassword',
                                                                                  'flatname': 'flat_name',
                                                                                  'admin': '12345678'})

    @patch("bot.flat.react.delete_flat")
    def test_delete_flat(self, delete_flat_mock):
        home_bot_cfg = HomeBot()
        message = generate_message("delete_flat name_of_flat")
        chat_id = message['chat']['id']
        with patch.object(home_bot_cfg.bot, 'sendMessage'):
            check_text_for_command_and_execute(home_bot_cfg, message)

        delete_flat_mock.assert_called_once_with(home_bot_cfg, chat_id, ['provenca', 'password'])

    # def test_founder_of_flat_can_delete(self):


    # @patch("bot.flat.api_actions.requests.post")
    # def test_endpoint_called(self, post_mock):
    #     home_bot_cfg = HomeBot()
    #     create_new_flat(home_bot_cfg, ['flat_name', 'itsapassword'])
    #
    #     post_mock.assert_called_once_with()
