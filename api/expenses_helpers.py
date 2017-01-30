# -*- coding: utf-8 -*-
from bson.objectid import ObjectId

from config import (mongo, SUCCESSFUL_VALIDATION_MESSAGE, USERNAME_NOT_AVAILABLE, AMOUNT_NOT_AVAILABLE,
                    DATE_NOT_AVAILABLE)
from user_helpers import update_total


def get_expense_list():
    response = []
    for expense in mongo.db.expenses.find():
        expense["_id"] = str(expense["_id"])
        response.append(expense)
    return response


def create_new_expense(data):
    status, error = validate_expense(data)
    username = data.get("username")
    user_obj = mongo.db.users.find_one({"username": username})
    total = user_obj["total"]
    if total is None:
        return False, "Error retrieving current total for user '{}'".format(username)
    if status:
        expense = mongo.db.expenses.insert(data)
        new_total = total + data["amount"]
        updated = update_total(username, new_total)
        if updated:
            return True, str(expense)
        else:
            return False, "Error updating the user '{}'".format("username")
    else:
        return False, error


def get_single_expense(_id):
    expense = mongo.db.expenses.find_one({"_id": ObjectId(_id)})
    expense["_id"] = str(expense["_id"])
    return expense


def update_expense(_id, new_data):
    print(new_data)
    result = mongo.db.expenses.update_one({"_id": ObjectId(_id)}, {'$set': new_data})
    result = result.raw_result
    print(result)
    if "ok" in result and result["ok"] == 1:
        return True
    else:
        return False


def delete_expense(_id):
    result = mongo.db.expenses.delete_one({"_id": ObjectId(_id)})
    result = result.raw_result
    if "ok" in result and result["ok"] == 1:
        return True
    else:
        return False


def validate_expense(expense):
    date = expense.get("date")
    if date is None:
        return False, DATE_NOT_AVAILABLE

    amount = expense.get("amount")
    if amount is None:
        return False, AMOUNT_NOT_AVAILABLE

    username = expense.get("username")
    if username is None:
        return False, USERNAME_NOT_AVAILABLE

    return True, SUCCESSFUL_VALIDATION_MESSAGE
