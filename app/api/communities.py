from app.api import bp
from flask import jsonify, request, url_for, g
from app.api.errors import bad_request, duplicate_resource_error, unauthorized_resource, resource_not_found
from app.models.user_model import User
from app.models.community_model import Community
from app.models.subscription_model import Subscription
from app.daos import community_dao, user_dao, chat_dao
from app import db
from app.api.auth import token_auth
from app.services import community_service

"""
Create a community

PAYLOAD REQUIRED: name, description
PAYLOAD OPTIONAL: invite_usernames (list), invite_uuids (list)
"""
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

    # Create subscription for creator/admin
    community_service.create_subscription(g.current_user, community, priveleges=1)

    # Create subscriptions for attached invite_usernames and invite_uuids
    if 'invite_usernames' in data:
        community_service.add_by_username(data['invite_usernames'], community)
    if 'invite_uuids' in data:
        community_service.add_by_uuid(data['invite_uuids'], community)

    response = jsonify(community.to_dict())
    response.status_code = 201

    return response

"""
Add other users to an existing community

PAYLOAD OPTIONAL: invite_usernames (list), invite_uuids (list)
"""
@bp.route('/communities/invite/<community_uuid>', methods=['PUT'])
@token_auth.login_required
def invite_subscriber(community_uuid):
    data = request.get_json() or {}

    community = community_dao.get_by_uuid(community_uuid)

    # Validations
    if not community:
        resource_not_found()
    if not g.current_user.is_subscribed(community):
        unauthorized_resource()

    # Create subscriptions for attached invite_usernames and invite_uuids
    if 'invite_usernames' in data:
        community_service.add_by_username(data['invite_usernames'], community)
    if 'invite_uuids' in data:
        community_service.add_by_uuid(data['invite_uuids'], community)

    response = jsonify(community.to_dict())
    response.status_code = 201

    return response

"""
Get all chat objects that pertain to a community that the user is a member of

URL PARAMETERS: community_uuid

Return: List of chat objects
"""
@bp.route('/communities/<community_uuid>/member_chats', methods=['GET'])
@token_auth.login_required
def list_member_chats(community_uuid):
    community = community_dao.get_by_uuid(community_uuid)

    # Validations
    if not community:
        resource_not_found()
    if not g.current_user.is_subscribed(community):
        unauthorized_resource()

    for membership in g.current_user.memberships:
        if membership.chat.community == community:
            chats.append(membership.chat.to_dict())

    response = jsonify(chats)

    response.status_code = 201

    return response

"""
Get a community by uuid

URL PARAMETERS: community_uuid

Return: Community object
"""
@bp.route('/communities/<community_uuid>', methods=['GET'])
@token_auth.login_required
def get_community(community_uuid):
    community = community_dao.get_by_uuid(community_uuid)

    # Validations
    if not community:
        resource_not_found()
    if not g.current_user.is_subscribed(community):
        unauthorized_resource()

    response = jsonify(community.to_dict())
    response.status_code = 200

    return response
