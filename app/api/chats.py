from app.api import bp
from flask import jsonify, request, url_for, g
from app.api.errors import bad_request
from app.models.user_model import User
from app.models.chat_model import Chat
from app import db
from app.daos import chat_dao, user_dao
from app.api.auth import token_auth
from datetime import datetime

"""
CREATE A CHAT

ARGUMENTS
 - Chat name (display name for the chat)
 - Members (usernames of other members to be added to the chat)

 RETURN
 - Chat object in json form
"""
@bp.route('/chats', methods=['POST'])
@token_auth.login_required
def create_chat():
    data = request.get_json() or {}

    # Data validation
    if 'name' not in data or 'members' not in data:
        return bad_request('must include name and members fields')

    chat = Chat()
    chat.from_dict(data)
    db.session.add(chat)
    db.session.commit()


    g.current_user.join_chat(chat)
    new_members = user_dao.get_users_by_username(data['members'])
    for mem in new_members:
        mem.join_chat(chat)

    g.current_user.join_chat(chat)
    db.session.commit()

    response = jsonify(chat.to_dict())
    response.status_code = 201

    return response

"""
ADD A USER TO AN EXISTING CHAT

ARGUMENTS
- Username of user to add to chat

RETURN
- Chat object in JSON form
"""
@bp.route('/chats/<int:id>', methods=['PUT'])
@token_auth.login_required
def add_user():
    data = request.get_json() or {}
    chat = get_chat_by_id(id)
    if g.current_user not in chat.members:
        return bad_request('user must be member of chat with given chat id number')

    if 'username' not in data or get_user_by_username(data['username']) is None:
        return bad_request('valid username must be provided')

    new_member = get_user_by_username(data['username'])
    new_member.join_chat(chat)
    db.session.commit()

    response = jsonify(chat.to_dict())
    response.status_code = 201

    return response


@bp.route('/chats/<int:id>', methods=['GET'])
@token_auth.login_required
def get_chat(id):
    chat = chat_dao.get_chat_by_id(id)
    if chat is None:
        return bad_request('not a valid chat id')
    if not g.current_user.is_member(chat):
        return bad_request('user not authorized for chat')

    response = jsonify(chat.to_dict())
    response.status_code = 200

    return response
