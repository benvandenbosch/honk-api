import os
basedir = os.path.abspath(os.path.dirname(__file__))

# Configurations settings for the Flask app defined as class variables in
# config object
class Config(object):

    # Used as a key for generating signatures & tokens
    SECRET_KEY = os.environ.get('SECRERT_KEY') or 'ha will not guess this'

    # Set the location of the db (used by Flask-SQLAlchemy extension)
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
    'sqlite:///' + os.path.join(basedir, 'app.db')

    # Disable signal to application each time change is made to db
    SQLALCHEMY_TRACK_MODIFICATIONS = False
