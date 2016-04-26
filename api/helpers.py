# -*- coding: utf-8 -*-

from config import (mongo, SUCCESSFUL_VALIDATION_MESSAGE, TOTAL_NOT_AVAILABLE, USERNAME_NOT_AVAILABLE,
                    USER_ALREADY_EXISTS)


def get_user_list():
    """ Gets a list of all the available users
    :return: list containing all the users
    """
    response = []
    for user in mongo.db.users.find():
        user["_id"] = str(user["_id"])
        response.append(user)
    return response


def create_new_user(data):
    """ Inserts a new user into the DB
    :param data: dict containing the information for the new user
    :return: created user object or None if there was information missing
    """
    status, error = validate_user(data)
    if status:
        user = mongo.db.users.insert(data)
        return True, str(user)
    else:
        return False, error


def get_single_user(username):
    """ Retrieves a single user from the DB
    :param username: username to retrieve
    :return: user object or None if the user does not exist
    """
    user = mongo.db.users.find_one({"username": username})
    user["_id"] = str(user["_id"])
    return user


def update_total(username, new_total):
    """ Updates the total for a user in the DB
    :param username: username to updated
    :param new_total: new total to use
    :return:
    """
    result = mongo.db.users.update_one({"username": username}, {'$set': {'total': new_total}})
    result = result.raw_result
    if "ok" in result and result["ok"] == 1:
        return True
    else:
        return False


def delete_user(username):
    """ Deletes a user from the DB
    :param username: username to be deleted
    :return: True if the deletion is successful or False otherwise
    """
    result = mongo.db.users.delete_one({"username": username})
    print(result.raw_result)
    result = result.raw_result
    if "ok" in result and result["ok"] == 1:
        return True
    else:
        return False


def validate_user(user):
    """ Validates that a new user to be created does not exist and does not have any missing information
    :param user: dict containing the data for the new user
    :return: True if the user is valid, False otherwise
    """
    username = user.get("username")
    if username is None:
        return False, USERNAME_NOT_AVAILABLE

    total = user.get("total")
    if total is None:
        return False, TOTAL_NOT_AVAILABLE

    if mongo.db.users.find_one({"username": username}):
        return False, USER_ALREADY_EXISTS

    return True, SUCCESSFUL_VALIDATION_MESSAGE
