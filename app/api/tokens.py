from flask import jsonify, g
from app import db
from app.api import bp
from app.api.auth import basic_auth, token_auth

# Authentication subsystem for API

# This function is only allowed if verification has been performed by
# verify_password function in auth.py as noted by @basic_auth.verify_password
# decorator
@bp.route('/tokens', methods=['POST'])
@basic_auth.login_required
def get_token():
    token = g.current_user.get_token()
    db.session.commit()
    return jsonify({'token': token})

# Revoke the token of the current user
@bp.route('/tokens', methods=['DELETE'])
@token_auth.login_required
def revoke_token():
    g.current_user.revoke_token()
    db.session.commit()
    return '', 204
