from app.api import bp
from flask import jsonify, request, url_for, g
from app.api.errors import bad_request, unauthorized_resource
from app.models.user_model import User
from app.models.chat_model import Chat
from app.models.community_model import Community
from app import db
from app.daos import chat_dao, user_dao, community_dao
from app.api.auth import token_auth
from datetime import datetime
import uuid

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

    # TODO: Impose community id validation on chat
    # Data validation
    if 'name' not in data or 'members' not in data:
        return bad_request('must include name, members')

    chat = Chat(uuid=str(uuid.uuid4()))
    chat.from_dict(data)
    db.session.add(chat)
    db.session.commit()

     # TODO: Impose community id validation on chat
    if 'community_name' in data:
        community = community_dao.get_community_by_name(data['community_name'])

        if community is None or not g.current_user.is_subscribed(community):
            return unauthorized_resource('Community does not exist or user is not subscribed')
        chat.community = community

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
@bp.route('/chats/invite/<chat_uuid>', methods=['PUT'])
@token_auth.login_required
def add_user(chat_uuid):
    data = request.get_json() or {}
    chat = chat_dao.get_chat_by_uuid(chat_uuid)

    if g.current_user not in chat.members:
        return bad_request('user must be member of chat with given chat id number')

    if 'username' not in data or user_dao.get_user_by_username(data['username']) is None:
        return bad_request('valid username must be provided')

    new_member = user_dao.get_user_by_username(data['username'])
    new_member.join_chat(chat)
    db.session.commit()

    response = jsonify(chat.to_dict())
    response.status_code = 201

    return response


"""
LIST ALL CHATS A USER IS A MEMBER OF

ARGUMENTS
- None

RETURN
- List of chat objects
"""
@bp.route('/chats', methods=['GET'])
@token_auth.login_required
def get_memberships():

    # Get a list of the user's chats
    chat_objects = g.current_user.chats
    chat_list = [chat.to_dict() for chat in chat_objects]

    return jsonify(chat_list)

@bp.route('/chats/<int:uuid>', methods=['GET'])
@token_auth.login_required
def get_chat(uuid):
    chat = chat_dao.get_chat_by_uuid(uuid)
    if chat is None:
        return bad_request('not a valid chat uuid')
    if not g.current_user.is_member(chat):
        return bad_request('user not authorized for chat')

    response = jsonify(chat.to_dict())
    response.status_code = 200

    return response
