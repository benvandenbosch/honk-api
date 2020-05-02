from flask import jsonify, g
from app.models.message_model import Message
from app.models.message_delivery_model import MessageDelivery
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
