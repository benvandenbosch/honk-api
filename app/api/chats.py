from app.api import bp
from flask import jsonify, request, url_for, g
from app.api.errors import bad_request, unauthorized_resource
from app.models.user_model import User
from app.models.chat_model import Chat
from app.models.community_model import Community
from app import db
from app.daos import chat_dao, user_dao, community_dao
from app.services import chat_service
from app.api.auth import token_auth
from datetime import datetime
import uuid

"""
CREATE A CHAT

PAYLOAD REQUIRED: name, community_uuid (can be blank)
PAYLOAD OPTIONAL: invite_usernames (list), invite_uuids (list)

 RETURN
 - Chat object in json form
"""
@bp.route('/chats', methods=['POST'])
@token_auth.login_required
def create_chat():
    data = request.get_json() or {}

    if 'name' not in data or 'community_uuid' not in data:
        return bad_request('must include name, community_uuid')

    community = community_dao.get_by_uuid(data['community_uuid'])

    if community and not g.current_user.is_subscribed(community):
        return unauthorized_resource()

    # Create the chat
    chat = Chat(community=community)
    chat.from_dict(data)

    # Add the creator to the chat
    chat_service.create_membership(g.current_user, chat)

    # Add any other requested users to the chat
    if 'invite_usernames' in data:
        chat_service.add_by_username(data['invite_usernames'], chat)
    if 'invite_uuids' in data:
        chat_service.add_by_uuid(data['invite_uuids'], chat)

    # Create and send the API response
    response = jsonify(chat.to_dict())
    response.status_code = 201

    return response

"""
ADD A USER TO AN EXISTING CHAT

PAYLOAD OPTIONAL: invite_usernames (list), invite_uuids (list)

RETURN
- Chat object in JSON form
"""
@bp.route('/chats/invite/<chat_uuid>', methods=['PUT'])
@token_auth.login_required
def add_user(chat_uuid):
    data = request.get_json() or {}
    chat = chat_dao.get_chat_by_uuid(chat_uuid)

    # Validations
    if not chat:
        resource_not_found()
    if not g.current_user.is_member(chat):
        return unauthorized_resource('user must be member of chat with given chat uuid number')


     # Add any requested users to the chat
    if 'invite_usernames' in data:
        chat_service.add_by_username(data['invite_usernames'], chat)
    if 'invite_uuids' in data:
        chat_service.add_by_uuid(data['invite_uuids'], chat)

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
# @bp.route('/chats', methods=['GET'])
# @token_auth.login_required
# def get_memberships():
#
#     # Get a list of the user's chats
#     chat_objects = g.current_user.chats
#     chat_list = [chat.to_dict() for chat in chat_objects]
#
#     return jsonify(chat_list)
#
# @bp.route('/chats/<int:uuid>', methods=['GET'])
# @token_auth.login_required
# def get_chat(uuid):
#     chat = chat_dao.get_chat_by_uuid(uuid)
#     if chat is None:
#         return bad_request('not a valid chat uuid')
#     if not g.current_user.is_member(chat):
#         return bad_request('user not authorized for chat')
#
#     response = jsonify(chat.to_dict())
#     response.status_code = 200
#
#     return response
