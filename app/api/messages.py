from app.api import bp
from flask import jsonify, request, url_for, g
from app.api.errors import bad_request, unauthorized_resource, resource_not_found
from app.models.user_model import User
from app.models.chat_model import Chat
from app.models.message_model import Message
from app import db
from app.daos import chat_dao, user_dao, message_dao
from app.api.auth import token_auth
from datetime import datetime
from sqlalchemy import desc
from app.services import notification_service, message_service
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

    if not chat:
        return resource_not_found('Must provide a chat uuid')
    if not g.current_user.is_member(chat):
        return bad_request('Must provide chat uuid for chat user is a member of')

    # Create the message and an associated delivery object for each recipient
    message = Message(author_uuid=g.current_user.uuid, chat_uuid=chat.uuid)
    message.from_dict(data)
    message_service.create_deliveries(g.current_user, message, chat)
    db.session.commit()

    # Send message notification to recipients
    message_service.send_message(sender=g.current_user, message=message, chat=chat)

    # Formulate and send the response
    response = jsonify(message.to_dict())
    response.status_code = 201

    return response

"""
Update a message

URL PARAMETERS: message_uuid

OPTIONAL PAYLOAD: 'is_delivered' (string bool)

Return: Updated message object
"""
@bp.route('/messages/<message_uuid>', methods=['PUT'])
@token_auth.login_required
def update_message(message_uuid):

    data = request.get_json() or {}

    # Get the message delivery
    delivery = message_dao.get_message_delivery(g.current_user.uuid, message_uuid)
    message = message_dao.get_by_uuid(message_uuid)

    # Validations
    if not message:
        resource_not_found()
    if not g.current_user.is_member(message.chat):
        unauthorized_resource('must be member of chat to read a message')

    # Update message delivery status to delivered
    if 'is_delivered' in data and data['is_delivered'] == 'True':
        delivery.is_delivered = True
        db.session.commit()

    response = jsonify(message.to_dict())
    response.status_code = 201

    return response

"""
Get a specific message by uuid

URL PARAMETERS: message uuid
"""
@bp.route('/messages/<message_uuid>', methods=['GET'])
@token_auth.login_required
def get_message(message_uuid):

    # Get the message
    message = message_dao.get_by_uuid(message_uuid)

    # Validations
    if not message:
        resource_not_found()
    if not g.current_user.is_recipient(message):
        unauthorized_resource()

    response = jsonify(message.to_dict())
    response.status_code = 200

    return response

"""
Get all messages sent to a user that the user has not read
"""
@bp.route('/messages/unread', methods=['GET'])
@token_auth.login_required
def get_unread_messages():

    # Get all unread messages for the user
    messages = message_dao.get_unread(g.current_user)
    response = jsonify([{'message': message.to_dict(),
     'chat_uuid': message.chat.uuid}  for message in messages])
    response.status_code =200

    return response


"""
Get all messages sent to a user
"""
@bp.route('/messages', methods=['GET'])
@token_auth.login_required
def get_messages():

    # Get all messages sent to a user
    messages = message_dao.get_unread(g.current_user)
    response = jsonify([message.to_dict() for message in messages])
    response.status_code = 200

    return response
