# -*- coding: utf-8 -*-

import random
import string


def generate_message(text):
    return {
        'text': text,
        'chat': {'type': 'test',
                 'id': random.randint(999,9999)
                 }
            }

def generate_random_user():
    return {
        "username": "".join(random.choice(string.ascii_letters) for _ in range(10)),
        "total": random.randint(5, 50),
        "_id": "".join(random.choice(string.hexdigits) for _ in range(24)).lower(),
        "flat": "".join(random.choice(string.ascii_letters) for _ in range(10))
    }
