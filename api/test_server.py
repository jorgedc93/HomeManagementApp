# -*- coding: utf-8 -*-
import os
import random
import tempfile
import unittest
import ujson

from unittest.mock import patch

from config import URL_BASE
from api import server
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
        """ Test that a GET to the users endpoint returns the correct values """
        random_users = generate_random_users(random.randint(1,10))
        with patch.object(server, "get_user_list", return_value=random_users):
            response = self.app.get(URL_BASE + "users/", follow_redirects=True)

        response_dict = ujson.loads(response.data.decode("utf-8"))

        self.assertIn("status", response_dict)
        self.assertEqual(response_dict["status"], "ok")

        self.assertIn("data", response_dict)
        self.assertEqual(response_dict["data"], random_users)

    def test_get_users_empty(self):
        """ Test that a GET to the users endpoint returns an error when there are no users """
        with patch.object(server, "get_user_list", return_value=[]):
            response = self.app.get(URL_BASE + "users/", follow_redirects=True)

        response_dict = ujson.loads(response.data.decode("utf-8"))

        self.assertIn("status", response_dict)
        self.assertEqual(response_dict["status"], "error")

        self.assertIn("message", response_dict)
        self.assertEqual(response_dict["message"], "No users available")

    def test_post_create_user(self):
        """ Test that a successful POST creates a user """
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
        """ Test that a wrong POST fails creating a user """
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

        self.assertIn("message", response_dict)

    def test_get_single_user_enpoint(self):
        """ Test that a correct GET with a username returns the user """
        random_user = generate_random_user()

        with patch.object(server, "get_single_user", return_value=random_user):
            response = self.app.get(URL_BASE + "users/{}/".format(random_user["username"]))

        response_dict = ujson.loads(response.data.decode("utf-8"))

        self.assertIn("status", response_dict)
        self.assertEqual(response_dict["status"], "ok")

        self.assertIn("data", response_dict)
        self.assertEqual(response_dict["data"], random_user)

    def test_get_single_user_enpoint_error(self):
        """ Test that a wrong GET with a username returns the user """
        random_user = generate_random_user()

        with patch.object(server, "get_single_user", return_value=None) as mock_get_user:
            response = self.app.get(URL_BASE + "users/{}/".format(random_user["username"]))
            self.assertEqual(mock_get_user.call_args[0][0], random_user["username"])

        response_dict = ujson.loads(response.data.decode("utf-8"))

        self.assertIn("status", response_dict)
        self.assertEqual(response_dict["status"], "error")

        self.assertIn("message", response_dict)
        self.assertEqual(response_dict["message"], "Unable to retrieve user '{}'".format(random_user["username"]))

    def test_put_update_total_endpoint(self):
        """ Test that a PUT request with a new total updates the user """
        random_user = generate_random_user()
        new_total = random.randint(5, 100)

        with patch.object(server, "update_total", return_value=True) as mock_update_total:
            url = URL_BASE + "users/{}/".format(random_user["username"])
            response = self.app.put(url, data=ujson.dumps(dict(total=new_total)), content_type='application/json')

            self.assertEqual(mock_update_total.call_args[0][0], random_user["username"])
            self.assertEqual(mock_update_total.call_args[0][1], new_total)

        response_dict = ujson.loads(response.data.decode("utf-8"))

        self.assertIn("status", response_dict)
        self.assertEqual(response_dict["status"], "ok")

        response_message = "User '{}' updated correctly with new total: {}".format(random_user["username"],
                                                                                   new_total)
        self.assertIn("message", response_dict)
        self.assertEqual(response_dict["message"], response_message)

    def test_error_put_update_total_endpoint(self):
        """ Test that a PUT request with a new total updates the user """
        random_user = generate_random_user()
        new_total = "I'm a wrong total"

        with patch.object(server, "update_total", return_value=False) as mock_update_total:
            url = URL_BASE + "users/{}/".format(random_user["username"])
            response = self.app.put(url, data=ujson.dumps(dict(total=new_total)), content_type='application/json')

            self.assertEqual(mock_update_total.call_args[0][0], random_user["username"])
            self.assertEqual(mock_update_total.call_args[0][1], new_total)

        response_dict = ujson.loads(response.data.decode("utf-8"))

        self.assertIn("status", response_dict)
        self.assertEqual(response_dict["status"], "error")

        response_message = "Error updating user '{}'".format(random_user["username"])
        self.assertIn("message", response_dict)
        self.assertEqual(response_dict["message"], response_message)

    def test_delete_user_endpoint(self):
        """ Test that a DELETE request removes the user """
        random_user = generate_random_user()

        with patch.object(server, "delete_user", return_value=True) as mock_delete_user:
            url = URL_BASE + "users/{}/".format(random_user["username"])
            response = self.app.delete(url, content_type='application/json')

            self.assertEqual(mock_delete_user.call_args[0][0], random_user["username"])

        response_dict = ujson.loads(response.data.decode("utf-8"))

        self.assertIn("status", response_dict)
        self.assertEqual(response_dict["status"], "ok")

        response_message = "User '{}' deleted correctly".format(random_user["username"])

        self.assertIn("message", response_dict)
        self.assertEqual(response_dict["message"], response_message)

    def test_error_delete_user_endpoint(self):
        """ Test that a wrong DELETE request returns an error """
        random_user = generate_random_user()

        with patch.object(server, "delete_user", return_value=False) as mock_delete_user:
            url = URL_BASE + "users/{}/".format(random_user["username"])
            response = self.app.delete(url, content_type='application/json')

            self.assertEqual(mock_delete_user.call_args[0][0], random_user["username"])

        response_dict = ujson.loads(response.data.decode("utf-8"))

        self.assertIn("status", response_dict)
        self.assertEqual(response_dict["status"], "error")

        response_message = "Error deleting user '{}'".format(random_user["username"])

        self.assertIn("message", response_dict)
        self.assertEqual(response_dict["message"], response_message)

if __name__ == '__main__':
    unittest.main()
