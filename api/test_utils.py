# -*- coding: utf-8 -*-

import random
import string


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


def generate_random_flat():
    flat = {
        "flatname": random_string(),
        "flat_members": ["dafuq"],
        "shopping_list": ["beer"]
    }
    return flat


def generate_random_user():
    """ Generates one valid random user
    :return: a rando valid user
    """
    return generate_random_users(1)[0]
