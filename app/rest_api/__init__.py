from flask import Blueprint

bp = Blueprint('rest-api', __name__)

from app.rest_api import users, errors, tokens
