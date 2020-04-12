from flask import jsonify
from app.models import Chat
from app import db

"""
Chat Data Access Object

Use this file to hold functions for querying the database for chat-related
functions
"""

# Get user by id
def get_chat_by_id(id):
    chat = Chat.query.get(id)
    return chat
