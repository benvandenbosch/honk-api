import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))

# Configurations settings for the Flask app defined as class variables in
# config object
class Config(object):

    # Used as a key for generating signatures & tokens
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'ha will not guess this'

    # Set the location of the db (used by Flask-SQLAlchemy extension)
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')

    print(SQLALCHEMY_DATABASE_URI)
    print(basedir)

    # Disable signal to application each time change is made to db
    SQLALCHEMY_TRACK_MODIFICATIONS = False
