from app import db
from datetime import datetime, timedelta
from app.models.user_model import User
from app.models.message_model import Message
from app.daos import user_dao
from app.models.message_delivery_model import MessageDelivery
import uuid


"""
Create MessageDelivery objects for each recipient of a message
"""
def create_deliveries(sender, message, chat):

    # Create message delivery objects for each recipient
    for membership in chat.memberships:
        member = membership.member

        # Default is_delivered should be false (unless member is sender)
        is_delivered = True if member == sender else False

        delivery = MessageDelivery(
            recipient = member,
            message = message,
            is_delivered = is_delivered,
            recipient_uuid = member.uuid,
            message_uuid = message.uuid
        )
        message.deliveries.append(delivery)
