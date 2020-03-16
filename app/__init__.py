from flask import Flask

honk = Flask(__name__)

from app import routes
