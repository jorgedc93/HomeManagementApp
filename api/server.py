# -*- coding: utf-8 -*-

from flask import request, jsonify

from api.config import app, URL_BASE
from api.exceptions import APIError
from api.expenses_helpers import (get_expense_list, create_new_expense, get_single_expense, update_expense,
                                  delete_expense)
from api.user_helpers import get_user_list, create_new_user, get_single_user, delete_user, update_total


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

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
