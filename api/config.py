# -*- coding: utf-8 -*-

from flask import Flask
from flask_pymongo import PyMongo

app = Flask("HomeManagementApp")
app.config["MONGO_DBNAME"] = "home_management_db"
mongo = PyMongo(app, config_prefix='MONGO')

URL_BASE = '/api/v1/'
