# -*- coding: utf-8 -*-

import requests
from unittest import TestCase

from api.test_utils import generate_random_flat

class ApiReadWrite(TestCase):
    """ DANGER! these tests will happily litter your DB
    """

    # def test_create_user(self):
    #     user = generate_random_user()
    #     print(user)
    #     response = requests.post('http://0.0.0.0:5000/api/v1/users/', json=user)
    #     print(response)
    #     self.assertEqual(response.status_code, 200)
    #
    #     response = requests.get('http://0.0.0.0:5000/api/v1/users')
    #     self.assertEqual(response.status_code, 200)
    #     print(response.json()['data'])

    # def test_get_single_user(self):
    #     username = 'cXjEWmKeHv'
    #
    #     response = requests.get('http://0.0.0.0:5000/api/v1/users/{}/'.format(username))
    #     print(response.json()['data'])
    #     self.assertEqual(response.status_code, 200)

    def test_create_get_delete_flat(self):
        flat = generate_random_flat()
        flatname = flat["flatname"]

        response = requests.post('http://0.0.0.0:5000/api/v1/flats/', json=flat)
        print()
        print(response.json()['data'])
        print()
        self.assertEqual(response.status_code, 200)

        response = requests.get('http://0.0.0.0:5000/api/v1/flats')
        print()
        print(response.json()['data'])
        print()
        self.assertEqual(response.status_code, 200)

        response = requests.get('http://0.0.0.0:5000/api/v1/flats/{}/'.format(flatname))
        print()
        print(response.json()['data'])
        print()
        self.assertEqual(response.status_code, 200)

        response = requests.delete('http://0.0.0.0:5000/api/v1/flats/{}/'.format(flatname))
        self.assertEqual(response.status_code, 200)


    # def test_get_single_flat(self):
    #     flatname = 'EYgGWhPLLe'
    #
    #     response = requests.get('http://0.0.0.0:5000/api/v1/flats/{}/'.format(flatname))
    #     print(response.json()['data'])
    #     self.assertEqual(response.status_code, 200)
    #
    # def test_delete_single_flat(self):
    #     flatname = 'EYgGWhPLLe'
    #
    #     response = requests.delete('http://0.0.0.0:5000/api/v1/flats/{}/'.format(flatname))
    #     print(response.json()['data'])
    #     self.assertEqual(response.status_code, 200)

    def test_replace_shopping_list(self):
        flat = generate_random_flat()
        flatname = flat["flatname"]

        response = requests.post('http://0.0.0.0:5000/api/v1/flats/', json=flat)
        print()
        print(response.json()['data'])
        print()
        self.assertEqual(response.status_code, 200)

        shopping_list ={
            'shopping_list': ["eggs", "butter"]
        }

        flat_members ={
            'flat_members': ["Me", "I"]
        }

        response = requests.get('http://0.0.0.0:5000/api/v1/flats/{}/'.format(flatname))
        print()
        print(response.json()['data'])
        print()
        self.assertEqual(response.status_code, 200)

        response = requests.put('http://0.0.0.0:5000/api/v1/flats/{}/shopping_list/'.format(flatname), json=shopping_list)
        self.assertEqual(response.status_code, 200)

        response = requests.put('http://0.0.0.0:5000/api/v1/flats/{}/members/'.format(flatname), json=flat_members)
        self.assertEqual(response.status_code, 200)

        response = requests.get('http://0.0.0.0:5000/api/v1/flats/{}/'.format(flatname))
        print()
        print(response.json()['data'])
        print()
        self.assertEqual(response.status_code, 200)

        response = requests.delete('http://0.0.0.0:5000/api/v1/flats/{}/'.format(flatname))
        self.assertEqual(response.status_code, 200)
