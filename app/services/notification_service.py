from flask import jsonify, g
from app import db, apns_client
from app.models.chat_model import Chat
from app.models.user_model import User
from app.models.message_model import Message
from app.models.community_model import Community
from app.models.membership_model import Membership
import os, json

"""
Notify the client in the background that a chat object has been updated
Category: update_chat
"""
def chat_update_notification(user, chat):

    extra = {
        'chat_uuid': chat.uuid
    }

    deliver_notification(user, extra=extra, category='chat')


"""
Notify the client in the background that a community has been updated
Category: update_community
"""
def community_update_notification(user, community):

    extra = {
        'community_uuid': community.uuid
    }

    deliver_notification(user, extra=extra, category='community')


"""
Notify users when they have been added to a community
"""
def new_community_notification(user, inviter, community):

    # Create the alert specificiations
    alert = {
        'title': 'New Community: ' + community.name,
        'subtitle': 'Invited by ' + inviter.username,
        'body': community.description
    }

    extra = {
        'community_uuid': community.uuid
    }

    deliver_notification(user, alert=alert, extra=extra, sound='default',
        category='community')


"""
Notify users when they have been added to a new chat
"""
def new_chat_notification(user, inviter, chat):

    # Create the alert specificiations
    alert = {
        'title': 'New Chat: ' + chat.name,
        'subtitle': 'Invited by ' + inviter.username
    }

    # Create the payload
    extra = {
        'community_uuid': None,
        'chat_uuid': chat.uuid
    }

    if chat.community:
        alert.update({'body': 'within ' + chat.community.name})
        extra.update({'community_uuid': chat.community.uuid})

    deliver_notification(user, alert=alert, extra=extra, sound='default',
        category='chat')


"""
Notify a user of a new reaction
Category: new_reaction
"""
def new_reaction_notification(user, reaction, message, sender):

    # Create the alert specifications:
    alert = {
        'subtitle': message.chat.name
    }

    # Change the verbiage depending on the reaction type
    if reaction.reaction_type == 'like':
        alert.update({'title': sender.username + ' liked a message'})

    extra = {
        'message_uuid': message.uuid
    }

    # Send the notification
    deliver_notification(user, alert=alert, extra=extra, sound='default',
        category='message')


"""
Notify all members of a chat when a new message is sent
"""
def new_message_notification(sender, user, message, chat):

    # Create the alert specifications
    alert = {
        'title': 'Message in ' + chat.name,
        'subtitle': sender.username,
        'body': message.content
    }

    # Create the payload
    extra = {
        'chat_uuid': chat.uuid,
    }

    deliver_notification(user, alert=alert, sound='default', category='message',
        extra=extra)


"""
Send a notifications to APNs servers
"""
def deliver_notification(user, alert={}, badge=None, sound=None, category=None,
    content_available=True, action_loc_key=None, loc_key=None, loc_args=[], extra={},
    identifier=None):

    if not os.environ.get('ENV_NAME') == 'PROD':
        return

    apns_client.send_message(
        registration_id = user.apns, # User-specific APNS token
        alert = alert,               # Visible notification parameters
        badge = badge,               # Update the badge on the app icon to this number
        sound = sound,               # String with name of sound file in Library/Sounds. Default is standard
        category = category,         # String value that represents notification type
        content_available = content_available, # Value of 1 wakes up app and delivers info to app delegate
        action_loc_key = action_loc_key,       # String - used as a key to find localized string to use with action
        loc_key = loc_key,           # Key to an alert-message string in Localizable.Strings
        loc_args = loc_args,         # Format specificers for loc_key
        extra = extra,               # Custom payload
        identifier = identifier,     # For grouping notifications
        expiration = None,           # Don't expire
        priority = 10,               # Priority 10 is sent immediately
        topic = None,                # Deprecated
    )
