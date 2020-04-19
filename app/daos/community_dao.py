from flask import jsonify
from app.models.community_model import Community
from app import db

"""
User Data Access Object

Use this file to hold functions for querying the database for user-related
functions
"""

# Get community by name
def get_community_by_name(name):
    return Community.query.filter_by(name=name).first()

def is_community(name):
    return Community.query.filter_by(name=name).count() > 0
