# -*- coding: utf-8 -*-
import os
import random
import tempfile
import unittest
import ujson

from mock import patch

from api.config import URL_BASE
from api import server
from api.test_utils import generate_random_user, generate_random_users


class ServerTestCase(unittest.TestCase):

    def setUp(self):
        self.db_fd, server.app.config['DATABASE'] = tempfile.mkstemp()
        server.app.config['TESTING'] = True
        self.app = server.app.test_client()

    def tearDown(self):
        os.close(self.db_fd)
        os.unlink(server.app.config['DATABASE'])

    def test_get_users_correct(self):
        """ Test that a get to the users endpoint returns the correct values """
        random_users = generate_random_users(random.randint(1,10))
        with patch.object(server, "get_user_list", return_value=random_users):
            response = self.app.get(URL_BASE + "users/", follow_redirects=True)

        response_dict = ujson.loads(response.data.decode("utf-8"))

        self.assertIn("status", response_dict)
        self.assertEqual(response_dict["status"], "ok")

        self.assertIn("data", response_dict)
        self.assertEqual(response_dict["data"], random_users)

    def test_get_users_empty(self):
        """ Test that a get to the users endpoint returns an error when there are no users """
        with patch.object(server, "get_user_list", return_value=[]):
            response = self.app.get(URL_BASE + "users/", follow_redirects=True)

        response_dict = ujson.loads(response.data.decode("utf-8"))

        self.assertIn("status", response_dict)
        self.assertEqual(response_dict["status"], "error")

        self.assertIn("response", response_dict)
        self.assertEqual(response_dict["response"], "No users available")

    def test_post_create_user(self):
        """ Test that a successful post creates a user """
        random_user = generate_random_user()

        with patch.object(server, "create_new_user", return_value=(True, str(random_user))):
            response = self.app.post(URL_BASE + "users/", data=ujson.dumps(random_user),
                                     content_type='application/json')

        response_dict = ujson.loads(response.data.decode("utf-8"))

        self.assertIn("status", response_dict)
        self.assertEqual(response_dict["status"], "ok")

        self.assertIn("data", response_dict)
        self.assertEqual(response_dict["data"], str(random_user))

    def test_wrong_post_failure(self):
        """ Test that a wrong post fails creating a user """
        random_user = generate_random_user()
        err_msg = "I'm an error message"

        with patch.object(server, "create_new_user", return_value=(False, err_msg)):
            response = self.app.post(URL_BASE + "users/", data=ujson.dumps(random_user),
                                     content_type='application/json')

        response_dict = ujson.loads(response.data.decode("utf-8"))

        self.assertIn("status", response_dict)
        self.assertEqual(response_dict["status"], "error")

        self.assertIn("error", response_dict)
        self.assertEqual(response_dict["error"], err_msg)

        response_msg = "Unable to create user with data: {}".format(random_user)
        self.assertIn("response", response_dict)
        self.assertEqual(response_dict["response"], response_msg)



if __name__ == '__main__':
    unittest.main()
