# -*- coding: utf-8 -*-

import random
import string
import unittest
from unittest.mock import patch

import helpers
from config import (app, SUCCESSFUL_VALIDATION_MESSAGE, TOTAL_NOT_AVAILABLE, USERNAME_NOT_AVAILABLE,
                    USER_ALREADY_EXISTS)


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


@patch("helpers.mongo")
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

    def test_validate_valid_user(self, mock_mongo):
        """ Test that a valid user returns True and Successful"""

        user = generate_random_users(1)[0]
        mock_mongo.db.users.find_one.return_value = None

        valid, message = helpers.validate_user(user)

        self.assertTrue(valid)
        self.assertEqual(message, SUCCESSFUL_VALIDATION_MESSAGE)

    def test_validate_user_without_username(self, mock_mongo):
        """ Test that a user without username returns False and a correct message"""

        user = generate_random_users(1)[0]
        del user["username"]

        valid, message = helpers.validate_user(user)

        self.assertFalse(valid)
        self.assertEqual(message, USERNAME_NOT_AVAILABLE)

    def test_validate_user_without_total(self, mock_mongo):
        """ Test that a user without total returns False and a correct message"""

        user = generate_random_users(1)[0]
        del user["total"]

        valid, message = helpers.validate_user(user)

        self.assertFalse(valid)
        self.assertEqual(message, TOTAL_NOT_AVAILABLE)

    def test_validate_user_already_exists(self, mock_mongo):
        """ Test that a user that already exists returns False and a correct message"""

        user = generate_random_users(1)[0]
        mock_mongo.db.users.find_one.return_value = user

        valid, message = helpers.validate_user(user)

        self.assertFalse(valid)
        self.assertEqual(message, USER_ALREADY_EXISTS)


if __name__ == "__main__":
    unittest.main()
