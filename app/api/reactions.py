from app.api import bp
from flask import jsonify, request, url_for, g
from app.api.errors import bad_request, resource_not_found, unauthorized_resource
from app.models.user_model import User
from app.models.chat_model import Chat
from app.models.message_model import Message
from app.models.reaction_model import Reaction
from app import db
from app.daos import chat_dao, user_dao, message_dao
from app.api.auth import token_auth
from datetime import datetime
from sqlalchemy import desc
from app.services import notification_service, message_service
import os, uuid

"""
Add a reaction to a message

URL PARAMETERS: message_uuid
PAYLOAD REQUIRED: reaction_type

RETURN: Message object in json form

TODO: Update reaction type validation as more reaction types are added
"""
@bp.route('/messages/<message_uuid>/reactions', methods=['POST'])
@token_auth.login_required
def add_reaction(message_uuid):
    data = request.get_json() or {}
    message = message_dao.get_by_uuid(message_uuid)

    # Validation
    if not 'reaction_type' in data or data['reaction_type'] not in ['like']:
        bad_request('Must provide a valid reaction type')
    if not message:
        resource_not_found()
    if not g.current_user.is_member(message.chat):
        unauthorized_resource()

    data['message_uuid'] = message_uuid

    # Create the reaction
    reaction = Reaction()
    reaction.from_dict(data)
    db.session.commit()

    message_service.send_reaction(sender=g.current_user, message=message, reaction=reaction)

    # Formulate and send the response
    response = jsonify(message.to_dict())
    response.status_code = 201

    return response

"""
Update a reaction

URL PARAMETERS: reaction_uuid

OPTIONAL PAYLOAD: reaction_type, is_delivered

Return: Updated message object
"""
@bp.route('/messages/reactions/<reaction_uuid>', methods=['PUT'])
@token_auth.login_required
def update_reaction(reaction_uuid):

    data = request.get_json() or {}

    # Get the message delivery
    delivery = message_dao.get_reaction_delivery(g.current_user.uuid, reaction_uuid)
    reaction = message_dao.get_reaction_by_uuid(reaction_uuid)

    # Validations
    if not reaction:
        resource_not_found()
    if not g.current_user.is_member(reaction.message.chat):
        unauthorized_resource()

    if 'reaction_type' in data and data['reaction_type'] not in ['like']:
        bad_request('Invalid reaction type')

    if 'reaction_type' in data:
        reaction.reaction_type = data['reaction_type']

    if data['is_delivered'] and data['is_delivered'] == 'True':
        delivery.is_delivered = True

    db.session.commit()

    response = jsonify(reaction.message.to_dict())
    response.status_code = 201

    return response
