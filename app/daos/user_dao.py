from flask import jsonify
from app.models import User
from app import db

"""
User Data Access Object

Use this file to hold functions for querying the database for user-related
functions
"""

# Get user by id
def get_user_by_id(id):
    user = User.query.get(id).first()
    return user

# Get user by username
def get_user_by_username(username):
    user = User.query.filter_by(username=username).first()
    return user
