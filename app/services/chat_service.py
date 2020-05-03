from app import db
from datetime import datetime, timedelta
from app.models.user_model import User
from app.models.membership_model import Membership
from app.daos import user_dao

"""
Create memberships in a chat given a list of usernames
"""
def add_by_username(usernames, chat):

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

    return


"""
Create memberships in a chat given a list of user uuids
"""
def add_by_uuid(uuids, chat):

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
