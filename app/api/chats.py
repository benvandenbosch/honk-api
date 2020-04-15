from app.api import bp
from flask import jsonify, request, url_for, g
from app.api.errors import bad_request
from app.models.user_model import User
from app.models.chat_model import Chat
from app import db
from app.daos import chat_dao, user_dao
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
        if new_member != None:
            new_member.join_chat(chat)
    g.current_user.join_chat(chat)
    db.session.commit()

    response = jsonify(chat.to_dict())
    response.status_code = 201

    return response

@bp.route('/chats/<int:id>', methods=['GET'])
@token_auth.login_required
def get_chat(id):
    chat = chat_dao.get_chat_by_id(id)
    if chat is None:
        return bad_request('not a valid chat id')
    if not g.current_user.is_member(chat):
        return bad_request('user not authorized for chat')

    return jsonify(chat.to_dict())
