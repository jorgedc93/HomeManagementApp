# -*- coding: utf-8 -*-

from api.config import mongo


def get_user_list():
    """ Gets a list of all the available users
    :return: list containing all the users
    """
    response = []
    for user in mongo.db.users.find():
        response.append(user)
    return response


def create_new_user(data):
    """ Inserts a new user into the DB
    :param data: dict containing the information for the new user
    :return: created user object or None if there was information missing
    """
    if validate_user(data):
        data["_id"] = data["username"]
        user = mongo.db.users.insert(data)
        return user
    else:
        return None


def get_single_user(username):
    """ Retrieves a single user from the DB
    :param username: username to retrieve
    :return: user object or None if the user does not exist
    """
    user = mongo.db.users.find_one({"username": username})
    return user


def update_user(username, data):
    pass


def delete_user(username):
    pass


def validate_user(user):
    """ Validates that a new user to be created does not exist and does not have any missing information
    :param user: dict containing the data for the new user
    :return: True if the user is valid, False otherwise
    """
    username = user.get("username")
    if not username:
        return False

    total = user.get("total")

    if not total:
        return False

    if mongo.db.users.find_one({"username": username}):
        return False

    return True
