# -*- coding: utf-8 -*-

from flask import request, jsonify, url_for, redirect

from api.config import app, URL_BASE
from api.helpers import get_user_list, create_new_user, get_single_user, delete_user, update_total


@app.route(URL_BASE + 'users', methods=['GET', 'POST'])
def users():
    """ Users endpoint"""
    if request.method == "GET":
        users = get_user_list()
        if users:
            return jsonify({"status": "ok", "data": users})
        else:
            return jsonify({"status": "error", "response": "No users available"})
    elif request.method == "POST":
        status, user = create_new_user(request.json)
        if status:
            return jsonify({"status": "ok", "data": user})
        else:
            return jsonify({"status": "error", "response": "Unable to create user with data: {}"
                           .format(request.json), "error": user})


@app.route(URL_BASE + 'users/<username>', methods=['GET', 'PUT', 'DELETE'])
def single_user(username):
    """ Single user endpoint"""
    if request.method == "GET":
        user = get_single_user(username)
        if user:
            return jsonify({"status": "ok", "data": user})
        else:
            return jsonify({"status": "error", "response": "Unable to retrieve user '{}'".format(username)})
    elif request.method == "PUT":
        if "total" in request.json:
            updated = update_total(username, request.json["total"])
            if updated:
                return jsonify({"status": "ok", "response": "User '{}' updated correctly with new total: {}"
                               .format(username, request.json["total"])})
            else:
                return jsonify({"status": "error", "response": "Error updating user '{}'".format(username)})
    elif request.method == "DELETE":
        delete_user(username)


@app.route('/')
def home():
    """ Home endpoint"""
    return redirect(url_for("users"))


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
