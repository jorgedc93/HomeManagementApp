# -*- coding: utf-8 -*-

from api.config import mongo, SUCCESSFUL_VALIDATION_MESSAGE, NAME_NOT_AVAILABLE, FLAT_ALREADY_EXISTS

def get_flat_list():
    """ Gets a list of all available flats
    :return: list containing all the flats
    """
    response = []
    for flat in mongo.db.flats.find():
        flat["_id"] = str(flat["_id"])
        response.append(flat)
    return response


def create_new_flat(data):
    """ Inserts a new flat into the DB
    :param data: dict containing the information for the new flat
    :return: created flat object or None if there was information missing
    """
    status, error = validate_flat(data)
    if status:
        user = mongo.db.flats.insert(data)
        return True, str(user)
    else:
        return False, error


def get_single_flat(flatname):
    """ Retrieves a single flat from the DB
    :param flatname: flatname to retrieve
    :return: flat object or None if the flat does not exist
    """
    flat = mongo.db.flats.find_one({"flatname": flatname})
    flat["_id"] = str(flat["_id"])
    return flat


def delete_flat(flatname):
    """ Deletes a flat from the DB
    :param flatname: flatname to be deleted
    :return: True if the deletion is successful or False otherwise
    """
    result = mongo.db.flats.delete_one({"flatname": flatname})
    result = result.raw_result
    if "ok" in result and result["ok"] == 1:
        return True
    else:
        return False


def update_flat_members(flatname, flat_members):
    """ Updates the shopping list of a flat in the DB
    :param flatname: name of the flat with the shopping list to be updated
    :param new_total: new total to use
    :return: True for success
    """
    print(flat_members)
    result = mongo.db.flats.update_one({"flatname": flatname}, {'$set': {'flat_members': flat_members}})
    result = result.raw_result
    if "ok" in result and result["ok"] == 1:
        return True
    else:
        return False


def validate_flat(flat):
    """ Validates that a new flat to be created does not exist and does not have any missing information
    :param flat: dict containing the data for the new flat
    :return: True if the flat is valid, False otherwise
    """
    flatname = flat.get("flatname")
    if flatname is None:
        return False, NAME_NOT_AVAILABLE

    shopping_list = flat.get("shopping_list")
    if not isinstance(shopping_list, list):
        return False, TypeError

    flat_members = flat.get("flat_members")
    if not isinstance(flat_members, list):
        return False, TypeError

    if mongo.db.flats.find_one({"flatname": flatname}):
        return False, FLAT_ALREADY_EXISTS

    return True, SUCCESSFUL_VALIDATION_MESSAGE
