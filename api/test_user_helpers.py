# -*- coding: utf-8 -*-

import random
import unittest
from unittest.mock import patch

from api import user_helpers
from api.config import (app, SUCCESSFUL_VALIDATION_MESSAGE, TOTAL_NOT_AVAILABLE, NAME_NOT_AVAILABLE,
                        USER_ALREADY_EXISTS)
from api.test_utils import generate_random_user, generate_random_users


@patch("api.user_helpers.mongo")
class TestUserHelpers(unittest.TestCase):

    def setUp(self):
        self.app_context = app.app_context()
        self.app_context.push()

    def tearDown(self):
        self.app_context.pop()

    def test_get_user_list(self, mock_mongo):
        """ Test that getting a user list works as expected """

        random_users = generate_random_users(random.randint(1, 10))

        mock_mongo.db.users.find.return_value = random_users

        response_users = user_helpers.get_user_list()

        # We assert that it returns the expected number of users
        self.assertEqual(len(random_users), len(response_users))

        # And we assert that the users are the same
        for user in response_users:
            self.assertIn(user, random_users)

    def test_create_new_user_successful(self, mock_mongo):
        """ Test that creating a user works as expected if the user is valid """

        random_user = generate_random_user()
        str_random_user = str(random_user)
        mock_mongo.db.users.insert.return_value = random_user

        with patch.object(user_helpers, "validate_user", return_value=(True, "")):
            created, result = user_helpers.create_new_user(random_user)

        self.assertTrue(created)
        self.assertEqual(result, str_random_user)

    def test_create_new_user_error(self, mock_mongo):
        """ Test that creating a user returns an error if the user is not valid """

        random_user = generate_random_user()
        err_msg = "I'm an error message"
        mock_mongo.db.users.insert.return_value = random_user

        with patch.object(user_helpers, "validate_user", return_value=(False, err_msg)):
            created, result = user_helpers.create_new_user(random_user)

        self.assertFalse(created)
        self.assertEqual(result, err_msg)

    def test_get_single_user(self, mock_mongo):
        """ Test that a single user can be retrieved by its username """

        random_user = generate_random_user()
        mock_mongo.db.users.find_one.return_value = random_user

        result = user_helpers.get_single_user(random_user["username"])

        self.assertEqual(result, random_user)
        self.assertEqual(mock_mongo.db.users.find_one.call_args[0][0], {"username": random_user["username"]})

    def test_update_total_successful(self, mock_mongo):
        """ Test that a user can be updated with a new total value """

        random_user = generate_random_user()
        random_total = random.randint(5, 100)
        update_ok_result_dict = {"ok": 1}

        mock_mongo.db.users.update_one.return_value.raw_result = update_ok_result_dict
        update_param_dict = {"username": random_user["username"]}, {'$set': {'total': random_total}}

        updated = user_helpers.update_total(random_user["username"], random_total)

        self.assertTrue(updated)
        self.assertEqual(mock_mongo.db.users.update_one.call_args[0], update_param_dict)

    def test_update_total_error(self, mock_mongo):
        """ Test that an error is properly handled when the update does not work as expected """

        random_user = generate_random_user()
        random_total = random.randint(5, 100)
        update_error_raw_result = {"ok": 0}

        mock_mongo.db.users.update_one.return_value.raw_result = update_error_raw_result

        updated = user_helpers.update_total(random_user["username"], random_total)

        self.assertFalse(updated)

    def test_delete_user_correct(self, mock_mongo):
        """ Test that a correct deletion works as expected """

        random_user = generate_random_user()
        delete_ok_raw_result = {"ok": 1}
        mock_mongo.db.users.delete_one.return_value.raw_result = delete_ok_raw_result

        deleted = user_helpers.delete_user(random_user["username"])

        self.assertTrue(deleted)
        self.assertEqual(mock_mongo.db.users.delete_one.call_args[0][0], {"username": random_user["username"]})

    def test_delete_user_error(self, mock_mongo):
        """ Test that an error when deleting a user is handled correctly """

        random_user = generate_random_user()
        delete_error_raw_result = {"ok": 0}
        mock_mongo.db.users.delete_one.return_value.raw_result = delete_error_raw_result

        deleted = user_helpers.delete_user(random_user["username"])

        self.assertFalse(deleted)

    def test_validate_valid_user(self, mock_mongo):
        """ Test that a valid user returns True and Successful """

        user = generate_random_users(1)[0]
        mock_mongo.db.users.find_one.return_value = None

        valid, message = user_helpers.validate_user(user)

        self.assertTrue(valid)
        self.assertEqual(message, SUCCESSFUL_VALIDATION_MESSAGE)

    def test_validate_user_without_username(self, mock_mongo):
        """ Test that a user without username returns False and a correct message """

        user = generate_random_users(1)[0]
        del user["username"]

        valid, message = user_helpers.validate_user(user)

        self.assertFalse(valid)
        self.assertEqual(message, NAME_NOT_AVAILABLE)

    def test_validate_user_without_total(self, mock_mongo):
        """ Test that a user without total returns False and a correct message """

        user = generate_random_users(1)[0]
        del user["total"]

        valid, message = user_helpers.validate_user(user)

        self.assertFalse(valid)
        self.assertEqual(message, TOTAL_NOT_AVAILABLE)

    def test_validate_user_already_exists(self, mock_mongo):
        """ Test that a user that already exists returns False and a correct message """

        user = generate_random_users(1)[0]
        mock_mongo.db.users.find_one.return_value = user

        valid, message = user_helpers.validate_user(user)

        self.assertFalse(valid)
        self.assertEqual(message, USER_ALREADY_EXISTS)


if __name__ == "__main__":
    unittest.main()
