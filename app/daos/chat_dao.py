from flask import jsonify, g
from app.models.chat_model import Chat
from app.models.membership_model import Membership
from app.models.user_model import User
from app import db
import datetime

"""
Chat Data Access Object

Use this file to hold functions for querying the database for chat-related
functions
"""

# Get user by id
def get_chat_by_uuid(chat_uuid):
    chat = Chat.query.filter_by(uuid=chat_uuid).first()
    return chat

"""
Get all of the chats that a user is a member of
"""
def get_by_user(user):
    chats = Chat.query.join(Membership).filter(Chat.membership.member==user).all()
    return chats

def get_by_user_and_community(user, community):
    community_chats = community.chats
    chats = []
    for chat in community_chats:
        if user.is_member(chat):
            chats.append(chat)
    return chats
