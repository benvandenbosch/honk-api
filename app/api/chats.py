from app.api import bp
from flask import jsonify, request, url_for, g
from app.api.errors import bad_request
from app.models import User
from app import db
from app import daos.user_dao as user_dao
from app.api.auth import token_auth
from datetime import datetime

@bp.route('/chats', methods=['POST'])
@token_auth.login_required
def create_chat():
    data = request.get_json() or {}

    # Data validation
    if 'name' not in data or 'members' not in data:
        return bad_request('must include name and members fields')

    chat = Chat()
    chat.from_dict(data)
    db.session.add(chat)
    db.session.commit()

    for member in data['members']:
        new_member = user_dao.get_user_by_username(member['username']).first()
        new_member.join_chat(chat)

    response = jsonify(chat.to_dict())
    response.status_code = 201

    return response

    return response
