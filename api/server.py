# -*- coding: utf-8 -*-

from flask import request, jsonify

from api.config import app, URL_BASE
from api.helpers import (get_user_list, create_new_user, get_single_user, delete_user, update_total, get_flat_list,
                         create_new_flat, get_single_flat, delete_flat, replace_shopping_list, update_flat_members)


@app.route(URL_BASE + 'users/', methods=['GET', 'POST'])
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


@app.route(URL_BASE + 'users/<username>/', methods=['GET', 'PUT', 'DELETE'])
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
        deleted = delete_user(username)
        if deleted:
            return jsonify({"status": "ok", "response": "User '{}' deleted correctly".format(username)})
        else:
            return jsonify({"status": "error", "response": "Error deleting user '{}'".format(username)})


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
