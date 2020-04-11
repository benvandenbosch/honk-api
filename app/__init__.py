from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


# Create instances of extensions with global scope
db = SQLAlchemy()
migrate = Migrate()

# Use the Config class from config.py module to create an instance of the app
def create_app(config_class=Config):

    # Create an instance of the application
    honk = Flask(__name__)

    # Use the config class to initalize the environment
    honk.config.from_object(Config)

    # Bind extension instances to the current application
    db.init_app(honk)
    migrate.init_app(honk, db)

    from app.main import bp as main_bp
    honk.register_blueprint(main_bp)

    from app.api import bp as api_bp
    honk.register_blueprint(api_bp, url_prefix='/api')

    return honk

from app import models
