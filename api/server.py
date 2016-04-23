# -*- coding: utf-8 -*-

from flask import request, jsonify

from api.config import app, URL_BASE
from api.helpers import get_user_list, create_new_user, get_single_user, update_user, delete_user


@app.route(URL_BASE + 'users', methods=['GET', 'POST'])
def users():
    """ Home endpoint"""
    if request.method == "GET":
        users = get_user_list()
        if users:
            return jsonify({"status": "ok", "data": users})
        else:
            return {"response": "No users available"}
    elif request.method == "POST":
        user = create_new_user()
        if user:
            return jsonify({"status": "ok", "data": user})


@app.route(URL_BASE + 'users/<username>', methods=['GET', 'POST', 'DELETE'])
def single_user():
    """ Home endpoint"""
    if request.method == "GET":
        get_single_user()
    elif request.method == "PUT":
        update_user()
    elif request.method == "DELETE":
        delete_user()

    return "This is the index page"


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
