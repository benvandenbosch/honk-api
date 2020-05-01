from app.api import bp
from flask import jsonify, request, url_for, g
from app.api.errors import bad_request, unauthorized_resource, resource_not_found
from app.models.user_model import User
from app.daos import user_dao
from app import db
from app.api.auth import token_auth


"""
Get user information by UUID
"""
@bp.route('/users/<user_uuid>', methods=['GET'])
@token_auth.login_required
def get_user(user_uuid):
    """
    Return a user based on their UUID
    """

    # Query the database for the requested user
    requested_user = user_dao.get_by_uuid(user_uuid)

    # If user does not exist, throw a 404
    if not requested_user:
        return resource_not_found()

    # If requested own info, return full user info, else guest user info
    if requested_user == g.current_user:
        response = jsonify(requested_user.to_dict())

    else:
        response = jsonify(requested_user.to_public_dict())


    response.status_code = 200
    return response
"""
Create a user

PAYLOAD REQUIRED: username, email, password, TODO: APNS
PAYLOAD OPTIONAL: display_name, biography

RETURN: New user object
"""
@bp.route('/users', methods=['POST'])
def create_user():
    data = request.get_json() or {}

    # Validations
    if 'username' not in data or 'email' not in data or 'password' not in data:
        return bad_request('must include username, email and password fields')
    if User.query.filter_by(username=data['username']).first():
        return bad_request('please use a different username')
    if User.query.filter_by(email=data['email']).first():
        return bad_request('please use a different email address')

    # Insert into database
    user = User()
    user.from_dict(data, new_user=True)
    db.session.add(user)
    db.session.commit()
    response = jsonify(user.to_dict())
    response.status_code = 201

    return response

"""
Update a user

PAYLOAD OPTIONAL: apns, display_name, biography TODO: email, username

RETURN: Updated user object
"""
@bp.route('/users/', methods=['PUT'])
@token_auth.login_required
def edit_user():
    """
    Update User values with payload values
    """
    data = request.get_json() or {}

    g.current_user.update(data)
    db.session.commit()

    response = jsonify(g.current_user.to_dict())
    response.status_code = 200

    return response
