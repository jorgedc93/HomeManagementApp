# -*- coding: utf-8 -*-
import os
import random
import tempfile
import unittest
import ujson

from mock import patch

from config import URL_BASE
import server
from test_utils import generate_random_user, generate_random_users


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


if __name__ == '__main__':
    unittest.main()
