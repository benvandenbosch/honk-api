from flask import jsonify, g
from app import db, apns_client
from app.models.chat_model import Chat
from app.models.user_model import User

def deliver_message_notification(sender, chat):

    for user in chat.members:
        apns_client.send_message(
            registration_id = user.apns,
            alert = {
                'title': 'New Message in ' + chat.name,
                'subtitle': 'From ' + sender.username
            },
            badge=None,
            sound='default',
            category=None,
            content_available=False,
            action_loc_key=None,
            loc_key=None,
            loc_args=[],
            extra={},
            identifier=None,
            expiration=None,
            priority=10,
            topic=None
        )
