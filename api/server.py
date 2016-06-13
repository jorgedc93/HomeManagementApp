# -*- coding: utf-8 -*-

from flask import request, jsonify

from api.config import app, URL_BASE
from api.exceptions import APIError
from api.expenses_helpers import (get_expense_list, create_new_expense, get_single_expense, update_expense,
                                  delete_expense)
from api.flat_helpers import update_flat_members, delete_flat, create_new_flat, get_flat_list, get_single_flat
from api.user_helpers import (get_user_list, create_new_user, get_single_user, delete_user, update_total,
                              replace_shopping_list)


@app.route(URL_BASE + 'users/', methods=['GET', 'POST'])
def users():
    """ Users endpoint"""
    if request.method == "GET":
        users = get_user_list()
        if users:
            return jsonify({"status": "ok", "data": users})
        else:
            raise APIError("No users available", payload=dict(status="error"), status_code=404)
            # return jsonify({"status": "error", "response": "No users available"})
    elif request.method == "POST":
        status, user = create_new_user(request.json)
        if status:
            return jsonify({"status": "ok", "data": user})
        else:
            raise APIError("Unable to create user with data: {}".format(request.json),
                           payload=dict(status="error", error=user))


@app.route(URL_BASE + 'users/<username>/', methods=['GET', 'PUT', 'DELETE'])
def single_user(username):
    """ Single user endpoint"""
    if request.method == "GET":
        user = get_single_user(username)
        if user:
            return jsonify({"status": "ok", "data": user})
        else:
            raise APIError("Unable to retrieve user '{}'".format(username), payload=dict(status="error"),
                           status_code=404)
    elif request.method == "PUT":
        if "total" in request.json:
            updated = update_total(username, request.json["total"])
            if updated:
                return jsonify({"status": "ok", "message": "User '{}' updated correctly with new total: {}"
                               .format(username, request.json["total"])})
            else:
                raise APIError("Error updating user '{}'".format(username), payload=dict(status="error"))
    elif request.method == "DELETE":
        deleted = delete_user(username)
        if deleted:
            return jsonify({"status": "ok", "message": "User '{}' deleted correctly".format(username)})
        else:
            raise APIError("Error deleting user '{}'".format(username), payload=dict(status="error"))


@app.route(URL_BASE + 'expenses/', methods=['GET', 'POST'])
def expenses():
    """ Expenses endpoint"""
    if request.method == "GET":
        expenses = get_expense_list()
        if expenses:
            return jsonify({"status": "ok", "data": expenses})
        else:
            raise APIError("No expenses avaliable", payload=dict(status="error"), status_code=404)

    elif request.method == "POST":
        status, expense = create_new_expense(request.json)
        if status:
            return jsonify({"status": "ok", "data": expense})
        else:
            raise APIError("Unable to create expense with data: {}".format(request.json),
                           payload=dict(status="error", error=expense))


@app.route(URL_BASE + 'expenses/<_id>/', methods=['GET', 'PUT', 'DELETE'])
def single_expense(_id):
    """ Single expenses endpoint"""
    if request.method == "GET":
        expense = get_single_expense(_id)
        if expense:
            return jsonify({"status": "ok", "data": expense})
        else:
            raise APIError("Unable to retrieve expense '{}'".format(_id), payload=dict(status="error"),
                           status_code=404)
    elif request.method == "PUT":
        updated = update_expense(_id, request.json)
        if updated:
            return jsonify({"status": "ok", "message": "Expense '{}' updated correctly with new values: {}"
                           .format(_id, request.json)})
        else:
            raise APIError("Error updating expense '{}'".format(_id), payload=dict(status="error"))
    elif request.method == "DELETE":
        deleted = delete_expense(_id)
        if deleted:
            return jsonify({"status": "ok", "message": "User '{}' deleted correctly".format(_id)})
        else:
            raise APIError("Error deleting user '{}'".format(_id), payload=dict(status="error"))


@app.route(URL_BASE + 'flats/', methods=['GET', 'POST'])
def flat():
    """ Flats endpoint"""
    if request.method == "GET":
        flats = get_flat_list()
        if flats:
            return jsonify({"status": "ok", "data": flats})
        else:
            return jsonify({"status": "error", "response": "No flats available"})
    elif request.method == "POST":
        status, flat = create_new_flat(request.json)
        if status:
            return jsonify({"status": "ok", "data": flat})
        else:
            return jsonify({"status": "error", "response": "Unable to create flat with data: {}"
                           .format(request.json), "error": flat})


@app.route(URL_BASE + 'flats/<flatname>/', methods=['GET', 'DELETE'])
def single_flat(flatname):
    """ Single flat endpoint"""
    if request.method == "GET":
        flat = get_single_flat(flatname)
        if flat:
            return jsonify({"status": "ok", "data": flat})
        else:
            return jsonify({"status": "error", "response": "Unable to retrieve flat '{}'".format(flatname)})
    elif request.method == "DELETE":
        deleted = delete_flat(flatname)
        if deleted:
            return jsonify({"status": "ok", "response": "User '{}' deleted correctly".format(flatname)})
        else:
            return jsonify({"status": "error", "response": "Error deleting user '{}'".format(flatname)})


@app.route(URL_BASE + 'flats/<flatname>/shopping_list/', methods=['PUT'])
def shopping_list(flatname):
    if request.method == "PUT":
        if "shopping_list" in request.json:
            shopping_list = replace_shopping_list(flatname, request.json["shopping_list"])
            if shopping_list:
                return jsonify({"status": "ok", "response": "Flat '{}' updated correctly with new total: {}"
                               .format(flatname, request.json["shopping_list"])})
            else:
                return jsonify({"status": "error", "response": "Error updating user '{}'".format(flatname)})


@app.route(URL_BASE + 'flats/<flatname>/members/', methods=['PUT'])
def members(flatname):
    if request.method == "PUT":
        if "flat_members" in request.json:
            flat_members = update_flat_members(flatname, request.json["flat_members"])
            if flat_members:
                return jsonify({"status": "ok", "response": "Flat '{}' updated correctly with new flat_members: {}"
                               .format(flatname, request.json["flat_members"])})
            else:
                return jsonify({"status": "error", "response": "Error updating user '{}'".format(flatname)})
    else:
        return jsonify({"status": "error", "response": "Error updating flat_members for '{}'".format(flatname)})

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
