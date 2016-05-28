# -*- coding: utf-8 -*-

from flask import Flask
from flask_pymongo import PyMongo

app = Flask("HomeManagementApp")
app.config["MONGO_DBNAME"] = "home_management_db"
mongo = PyMongo(app, config_prefix='MONGO')

URL_BASE = '/api/v1/'

# Validation messages for users
SUCCESSFUL_VALIDATION_MESSAGE = "Successful"
USERNAME_NOT_AVAILABLE = "Username field not available"
TOTAL_NOT_AVAILABLE = "Total field not available"
DATE_NOT_AVAILABLE = "Date field not available"
AMOUNT_NOT_AVAILABLE = "Amount field not available"
USER_ALREADY_EXISTS = "User already exists"
