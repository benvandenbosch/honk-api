from app import db
from datetime import datetime, timedelta
from app.models.user_model import User
from app.models.message_model import Message
from app.daos import user_dao
from app.models.message_delivery_model import MessageDelivery
import uuid, os
from app.services import notification_service
from gobiko.apns.exceptions import BadDeviceToken, InvalidProviderToken

"""
Send a notification to recipients of a message
"""
def send_message(sender, message, chat):

    for membership in chat.memberships:
        if membership.member != sender:
            try:
                notification_service.new_message_notification(sender=sender,
                    user=membership.member, message=message, chat=chat)
            except (BadDeviceToken, InvalidProviderToken):
                print('Bad APNs token for ' + membership.member.username)


"""
Send a reaction to recipients of a message
"""
def send_reaction(sender, message, reaction):

    for delivery in reaction.deliveries:
        if delivery.recipient != sender:
            try:
                notification_service.new_reaction_notification(delivery.recipient, reaction, message, sender)
            except (BadDeviceToken, InvalidProviderToken):
                 print('Bad APNs token for ' + delivery.recipient.username)
                 pass

"""
Set all message deliveries to false except for the editor
"""
def reset_deliveries(editor, message):
    for delivery in message.deliveries:
        if delivery.recipient != editor:
            delivery.is_delivered = False
    db.session.commit()


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
            message_uuid = message.uuid,
            uuid = uuid.uuid4().hex
        )
        message.deliveries.append(delivery)
