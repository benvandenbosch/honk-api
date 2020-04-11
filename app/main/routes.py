from app.main import bp
from flask import current_app

@bp.route('/')
@bp.route('/index')
def index():
    return "Hello, Honk!"
