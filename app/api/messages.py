from app.api import bp
from flask import jsonify, request, url_for, g
from app.api.errors import bad_request
from app.models.user_model import User
from app.models.chat_model import Chat
from app.models.message_model import Message
from app import db
from app.daos import chat_dao, user_dao
from app.api.auth import token_auth
from datetime import datetime
from sqlalchemy import desc
from app.services import notification_service
import os, uuid

"""
SEND A MESSAGE

PAYLOAD REQUIRED: chat_uuid, content

 RETURN: Message object in json form
"""
@bp.route('/messages', methods=['POST'])
@token_auth.login_required
def send_message():
    data = request.get_json() or {}

    # Data validation
    if 'chat_uuid' not in data or 'content' not in data:
        return bad_request('must include chat_uuid and content fields')

    chat = chat_dao.get_chat_by_uuid(data['chat_uuid'])

    if not g.current_user.is_member(chat):
        return bad_request('Must provide chat uuid for chat user is a member of')

    message = Message()
    message.from_dict(data)
    db.session.commit()

    # message.author = g.current_user
    # message.chat = chat
    # db.session.add(message)
    # db.session.commit()
    # db.session.refresh(message)

    response = jsonify(message.to_dict())
    response.status_code = 201

    if os.environ.get('ENV_NAME') == 'PROD':
        notification_service.deliver_message_notification(sender=g.current_user,chat=chat)

    return response

"""
Get all messages for a user by chat id

"""
@bp.route('/messages/<chat_uuid>', methods=['GET'])
@token_auth.login_required
def get_chat_messages(chat_uuid):
    chat = chat_dao.get_chat_by_uuid(chat_uuid)

    if g.current_user not in chat.members:
        return bad_request('user must be member of chat with given chat uuid number')

    messages = Message.query.filter_by(chat_uuid=chat_uuid).order_by(desc(Message.created_at)).all()

    response = jsonify([message.to_dict() for message in messages])
    response.status_code = 200

    return response

"""
Get all messages for a user regardless of chat
"""
@bp.route('/messages', methods=['GET'])
@token_auth.login_required
def get_messages():
    # Get all the ids for chats the user is a part
    chat_ids = [chat.id for chat in g.current_user.chats]
    messages = Message.query.filter(Message.chat_id.in_(chat_ids)).order_by(desc(Message.created_at)).all()
    response = jsonify([message.to_dict() for message in messages])
    response.status_code = 200

    return response
