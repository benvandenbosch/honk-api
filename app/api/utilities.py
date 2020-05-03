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
Load all data available to client user
"""
@bp.route('/utilities/data', methods=['GET'])
@token_auth.login_required
def get_all_data():

    communities = community_dao.list_by_user(g.current_user)
    data = {
        'communities': [community.to_dict() for community in communities],
        'user': g.current_user.to_summary_dict()
    }

    response = jsonify(data)
    response.status_code = 200

    return response
