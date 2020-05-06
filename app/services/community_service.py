from app import db
from app.models.user_model import User
from app.models.community_model import Community
from app.models.subscription_model import Subscription
from app.daos import user_dao
from datetime import datetime, timedelta
from app.services import notification_service

"""
Create subscriptions to a community for each username in a given list of
usernames
"""
def add_by_username(inviter, usernames, community):

    # Retrive user objects for all usernames
    users = user_dao.get_users_by_username(usernames)

    # Iterate through user objects, adding subscriptions for those that don't
    # have them already
    for user in users:
        if not user.is_subscribed(community=community):
            create_subscription(user, community)
            notification_service.new_community_notification(user, inviter, community)

    return


"""
Create subscriptions to a community for each uuid in a given list of uuids
"""
def add_by_uuid(inviter, uuids, community):

    # Retrive user objects for all usernames
    users = user_dao.list_by_uuid(uuids)

    # Iterate through user objects, adding subscriptions for those that don't
    # have them already
    for user in users:
       if not user.is_subscribed(community=community):
           create_subscription(user, community)
           notification_service.new_community_notification(user, inviter, community)
    return


"""
Subscribe a user to a community given a user and community object
"""
def create_subscription(user, community, priveleges=0):
    subscription = Subscription(
        priveleges = priveleges,
        is_active = True,
        subscriber = user,
        community = community,
        created_at = datetime.utcnow(),
        community_uuid = community.uuid,
        user_uuid = user.uuid
    )
    db.session.commit()
