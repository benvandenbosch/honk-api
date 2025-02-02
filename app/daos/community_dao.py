from flask import jsonify
from app.models.community_model import Community
from app.models.chat_model import Chat
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

"""
Return a list of community objects given list of uuids
"""
def list_by_uuid(uuids):
    return Community.query.filter(Community.uuid.in_(uuids)).all()

"""
Returns a single community by uuid
"""
def get_by_uuid(uuid):
    return Community.query.filter_by(uuid=uuid).first()

"""
Get all communities a user is subscribed to
"""
def list_by_user(user):
    communities = [subscription.community for subscription in user.subscriptions]
    return communities

"""
Return a bool representing whether a community name is already taken
"""
def is_name_taken(name):
    return Community.query.filter_by(name=name).count() > 0


"""
Return a bool representing whether a chat name is already taken within a community
"""
def is_chat_name_taken(chat, name):
    return Chat.query.filter_by(community=chat.community).filter_by(name=name).count() > 0
