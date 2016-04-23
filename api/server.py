# -*- coding: utf-8 -*-

from flask import Flask, url_for, redirect, request
from flask_pymongo import PyMongo

app = Flask(__name__)
app.config["MONGO_DBNAME"] = "students_db"
mongo = PyMongo(app, config_prefix='MONGO')


@app.route('/')
def index():
    """ Home endpoint"""
    return "This is the index page"

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
