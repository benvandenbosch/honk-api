from app.api import bp
from flask import jsonify, request, url_for, g
from app.api.errors import bad_request, duplicate_resource_error
from app.models.user_model import User
from app.models.community_model import Community
from app.models.subscription_model import Subscription
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
    subscription.user = g.current_user
    community.subscriptions.append(subscription)
    db.session.commit()


    response = jsonify(community.to_dict())
    response.status_code = 201

    return response
