from app.api import bp
from flask import jsonify, request, url_for
from app.api.errors import bad_request
from app.models import User
from app import db


@bp.route('/users/<int:id>', methods=['GET'])
def get_user(id):
    """
    Return a user based on their ID
    """
    return jsonify(User.query.get_or_404(id).to_dict())

@bp.route('/users', methods=['POST'])
def create_user():
    data = request.get_json() or {}
    if 'username' not in data or 'email' not in data or 'password' not in data:
        return bad_request('must include username, email and password fields')
    if User.query.filter_by(username=data['username']).first():
        return bad_request('please use a different username')
    if User.query.filter_by(email=data['email']).first():
        return bad_request('please use a different email address')

    user = User()
    user.from_dict(data, new_user=True)
    db.session.add(user)
    db.session.commit()
    response = jsonify(user.to_dict())
    response.status_code = 201
    response.headers['Location'] = url_for('api.get_user', id=user.id)

    return response


@bp.route('/users/<int:id>', methods=['PUT'])
def update_user(id):
    pass
