from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


honk = Flask(__name__)

# Use the Config class from config.py module to cofigure the app environment
honk.config.from_object(Config)

# Create database & database migration instances
db = SQLAlchemy(honk)
migrate = Migrate(honk, db)

from app import routes, models
