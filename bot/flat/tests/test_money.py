# -*- coding: utf-8 -*-

import unittest
import random
from unittest.mock import patch

from bot.flat.react import check_text_for_command_and_execute
from bot.flat.home_bot import HomeBot
from bot.flat.tests.utils import generate_message



class MoneyTestCase(unittest.TestCase):

    @patch("bot.flat.react.update_balance")
    def test_update_balance(self, create_flat_mock):
        home_bot_cfg = HomeBot()
        expected_value = random.uniform(1,100)
        message = generate_message("put {}".format(expected_value))
        with patch.object(home_bot_cfg.bot, 'sendMessage'):
            check_text_for_command_and_execute(home_bot_cfg, message)
        create_flat_mock.assert_called_once_with(home_bot_cfg, message['chat']['id'], [str(expected_value)])
