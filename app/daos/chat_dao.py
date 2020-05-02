from flask import jsonify, g
from app.models.chat_model import Chat
from app.models.membership_model import Membership
from app import db

"""
Chat Data Access Object

Use this file to hold functions for querying the database for chat-related
functions
"""

# Get user by id
def get_chat_by_uuid(chat_uuid):
    chat = Chat.query.filter_by(uuid=chat_uuid).first()
    return chat
