from app.api import bp
from flask import jsonify, request, url_for, g
from app.api.errors import bad_request, duplicate_resource_error, unauthorized_resource
from app.models.user_model import User
from app.models.community_model import Community
from app.models.subscription_model import Subscription
from app.daos import community_dao, user_dao
from app import db
from app.api.auth import token_auth

@bp.route('/communities', methods=['POST'])
@token_auth.login_required
def create_community():
    data = request.get_json() or {}
    if 'name' not in data or 'description' not in data:
        return bad_request('Must include a name and description for the community')
    if Community.query.filter_by(name=data['name']).first() != None:
        return duplicate_resource_error('Community name already taken')

    community = Community()
    community.from_dict(data)
    subscription = Subscription(priveleges=1) # Creator should be an admin
    subscription.subscriber = g.current_user
    subscription.inviter = g.current_user
    community.subscriptions.append(subscription)
    db.session.commit()


    response = jsonify(community.to_dict())
    response.status_code = 201

    return response

@bp.route('/communities/invite', methods=['PUT'])
@token_auth.login_required
def invite_subscriber():
    data = request.get_json() or {}
    if 'username' not in data or 'community_name' not in data:
         return bad_request('Must include a username and community name')

    community = community_dao.get_community_by_name(data['community_name'])
    if community == None or not g.current_user.is_subscribed(community):
        return unauthorized_resource('User not subscribed to this community or it does not exist')

    invitee = user_dao.get_user_by_username(data['username'])

    if invitee == None or invitee.is_subscribed(community):
        return bad_request('User already subscribed or does not exist')

    subscription = Subscription(priveleges=0)
    subscription.subscriber = invitee
    subscription.community = community
    g.current_user.invitations.append(subscription)
    db.session.commit()

    response = jsonify(community.to_dict())
    response.status_code = 201

    return response
