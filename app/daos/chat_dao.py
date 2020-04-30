from flask import jsonify, g
from app.models.chat_model import Chat
from app import db

"""
Chat Data Access Object

Use this file to hold functions for querying the database for chat-related
functions
"""

# Get user by id
def get_chat_by_uuid(uuid):
    chat = Chat.query.filter_by(uuid=uuid).first()
    return chat
