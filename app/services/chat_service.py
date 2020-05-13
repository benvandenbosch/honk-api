from app import db
from datetime import datetime, timedelta
from app.models.user_model import User
from app.models.membership_model import Membership
from app.models.chat_model import Chat
from app.services import notification_service
from app.daos import user_dao
import os
from app.services import notification_service
from gobiko.apns.exceptions import BadDeviceToken, InvalidProviderToken

"""
Create initial automatic chat without new chat notification
"""
def make_first_chat(community):

    # Create the chat object and associate it with the community
    chat = Chat(community=community, community_uuid=community.uuid)
    chat.from_dict({'name': 'everyone'})
    db.session.commit()

    # Add all subscribers for the given community into the chat
    for subscription in community.subscriptions:
        create_membership(subscription.subscriber, chat)

    db.session.commit()


"""
Deliver chat updates to subscribers
"""
def send_updates(chat):

    for membership in chat.memberships:
        try:
            notification_service.chat_update_notification(membership.member, chat)
        except (BadDeviceToken, InvalidProviderToken):
            print('Bad APNs token for ' + membership.member.username)


"""
Create memberships in a chat given a list of usernames
"""
def add_by_username(inviter, usernames, chat):

    # Retrieve the user objects for all usernames
    users = user_dao.get_users_by_username(usernames)

    # Iterate through user objects, adding subscriptions for those that don't
    # have them already
    for user in users:

        # If the chat is part of a community, make sure the user is subscribed
        if chat.community:
            if not user.is_subscribed(chat.community):
                continue

        if not user.is_member(chat=chat):
            create_membership(user, chat)

        try:
            notification_service.new_chat_notification(user, inviter, chat)
        except (BadDeviceToken, InvalidProviderToken):
            print('Bad APNs token for ' + user.username)

    return


"""
Create memberships in a chat given a list of user uuids
"""
def add_by_uuid(inviter, uuids, chat):

    # Retrieve the user objects for all usernames
    users = user_dao.list_by_uuid(uuids)

    # Iterate through user objects, adding subscriptions for those that don't
    # have them already
    for user in users:

        # If the chat is part of a community, make sure the user is subscribed
        if chat.community:
            if not user.is_subscribed(community):
                continue

        if not user.is_member(chat=chat):
            create_membership(user, chat)

        try:
            notification_service.new_chat_notification(user, inviter, chat)
        except (BadDeviceToken, InvalidProviderToken):
            print('Bad APNs token for ' + user.username)

    return


"""
Given a user and a chat, create a membership
"""
def create_membership(user, chat):
    membership = Membership(
        member = user,
        chat = chat,
        created_at = datetime.utcnow(),
        is_active = True,
        user_uuid = user.uuid,
        chat_uuid = chat.uuid
    )
    db.session.commit()
