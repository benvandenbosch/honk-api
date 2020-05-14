from flask import jsonify, g
from app.models.message_model import Message
from app.models.reaction_model import Reaction
from app.models.chat_model import Chat
from app.models.message_delivery_model import MessageDelivery
from app.models.reaction_delivery_model import ReactionDelivery
from app import db
import datetime

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

"""
Get all unread messages for a user
"""
def get_unread(user):
    deliveries = MessageDelivery.query.filter_by(recipient=user).filter_by(is_delivered=False).all()
    messages = [delivery.message for delivery in deliveries]
    return messages

"""
Get all messages sent to a user
"""
def get_messages(user):
    deliveries = MessageDelivery.query.filter_by(recipient=user).all()
    messages = [delivery.message for delivery in deliveries]
    return messages

"""
Count messages created between now and given time in past
"""
def count_by_chat(chat, delta=datetime.timedelta(weeks=1)):

    # Get earliest datetime for acceptable created_at period
    start_date = datetime.datetime.utcnow() - delta

    # Count messages in given chat created between start date and now
    count = Message.query.filter_by(chat=chat).filter(Message.created_at > start_date).count()

    return count

"""
Generate % change in message activity levels for previous day and today
"""
def generate_activity_delta(chat):

    # Get datetime for start of 2 days ago and 1 day ago
    first_day_start = datetime.datetime.utcnow() - datetime.timedelta(days=2)
    second_day_start = datetime.datetime.utcnow() - datetime.timedelta(days=1)

    # Get volume of messages for each day
    first_day_volume = Message.query.filter_by(chat=chat).filter(
        Message.created_at > first_day_start).filter(Message.created_at < second_day_start).count()

    second_day_volume = Message.query.filter_by(chat=chat).filter(
        Message.created_at > second_day_start).count()

    # Calculate percentage change
    if first_day_volume == 0:
        return 100

    change = 100 * (second_day_volume / first_day_volume)

    return change

"""
Return most active user in a past week
"""
def get_most_active_username(chat):
    highest_user = ''
    max_count = 0
    start_date = datetime.datetime.utcnow() - datetime.timedelta(weeks=1)
    for membership in chat.memberships:
        member = membership.member
        member_count = Message.query.filter(Message.created_at > start_date).filter(
            Message.author == member).count()
        if member_count > max_count:
            highest_user = member.username
    return highest_user
