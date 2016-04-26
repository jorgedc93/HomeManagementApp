# -*- coding: utf-8 -*-

import random
import string
import unittest
from unittest.mock import patch

from api import helpers
from api.config import app


def random_string(length=10, chars=string.ascii_letters):
    """ Generates a random string
    :param length: desired length of the string
    :param chars: charset to use for the random string
    :return: a random string
    """
    return "".join(random.choice(chars) for _ in range(length))


def generate_random_users(num):
    """ Generates a list of random users
    :param num: number of users to generate
    :return: list of random valid users
    """
    users = []
    for i in range(num):
        user = {
            "username": random_string(),
            "total": random.randint(5, 50),
            "_id": random_string(length=24, chars=string.hexdigits).lower()
        }
        users.append(user)
    return users


@patch("api.helpers.mongo")
class TestHelpers(unittest.TestCase):

    def setUp(self):
        self.app_context = app.app_context()
        self.app_context.push()

    def tearDown(self):
        self.app_context.pop()

    def test_get_user_list(self, mock_mongo):
        """ Test that getting a user list works as expected """

        random_users = generate_random_users(random.randint(1, 10))

        mock_mongo.db.users.find.return_value = random_users

        response_users = helpers.get_user_list()

        # We assert that it returns the expected number of users
        self.assertEqual(len(random_users), len(response_users))

        # And we assert that the users are the same
        for user in response_users:
            self.assertIn(user, random_users)

if __name__ == "__main__":
    unittest.main()
