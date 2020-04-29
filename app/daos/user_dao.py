from flask import jsonify, g
from app.models.user_model import User
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

# Get multiple users by username
def get_users_by_username(usernames):
    users = User.query.filter(User.username.in_(usernames)).all()
    return users

# Return whether or not a provided username is valid (whether a user by that username exists)
def is_user(username):
    return User.query.filter_by(username=username).count() > 0
