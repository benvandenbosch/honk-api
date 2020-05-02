from flask import jsonify, g
from app.models.message_model import Message
from app.models.reaction_model import Reaction
from app.models.message_delivery_model import MessageDelivery
from app.models.reaction_delivery_model import ReactionDelivery
from app import db

"""
Query the db for a message by message uuid
"""
def get_by_uuid(message_uuid):
    return Message.query.filter_by(uuid=message_uuid).first()


"""
Get message delivery model by recipient and message uuids
"""
def get_message_delivery(user_uuid, message_uuid):
    return MessageDelivery.query.filter_by(recipient_uuid=user_uuid).filter_by(message_uuid=message_uuid).first()

"""
Get reaction delivery model by recipient and reaction uuids
"""
def get_reaction_delivery(user_uuid, reaction_uuid):
    return ReactionDelivery.query.filter_by(recipient_uuid=user_uuid).filter_by(reaction_uuid=reaction_uuid).first()

"""
Get reaction by reaction uuid
"""
def get_reaction_by_uuid(reaction_uuid):
    return Reaction.query.filter_by(uuid=reaction_uuid).first()
