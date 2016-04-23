# -*- coding: utf-8 -*-

from flask import request, jsonify, url_for, redirect

from api.config import app, URL_BASE
from api.helpers import get_user_list, create_new_user, get_single_user, update_user, delete_user


@app.route(URL_BASE + 'users', methods=['GET', 'POST'])
def users():
    """ Users endpoint"""
    if request.method == "GET":
        users = get_user_list()
        if users:
            return jsonify({"status": "ok", "data": users})
        else:
            return jsonify({"response": "No users available"})
    elif request.method == "POST":
        user = create_new_user(request.json)
        if user:
            return jsonify({"status": "ok", "data": user})
        else:
            return jsonify({"response": "Unable to create user with data: {}".format(request.json)})


@app.route(URL_BASE + 'users/<username>', methods=['GET', 'POST', 'DELETE'])
def single_user(username):
    """ Single user endpoint"""
    if request.method == "GET":
        user = get_single_user(username)
        if user:
            return jsonify({"status": "ok", "data": user})
        else:
            return jsonify({"response": "Unable to retrieve user '{}'".format(username)})
    elif request.method == "PUT":
        update_user(username, request.json)
    elif request.method == "DELETE":
        delete_user(username)


@app.route('/')
def home():
    """ Home endpoint"""
    return redirect(url_for("users"))


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
