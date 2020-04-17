from app import db
from datetime import datetime, timedelta

subscriptions = db.Table(
    'subscriptions',
    db.Column('subscriber_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('community_id', db.Integer, db.ForeignKey('community.id'))

)

class Community(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), index=True, unique=True)
    description = db.Column(db.String(500))
    created_at = db.Column(db.Column(db.DateTime, default=datetime.utcnow))

    # Many to many relationship with user (Subscription as association object)
    subscribers = db.relationship("Subscription", backref="community", lazy='dynamic')

    # One to many relationship with chats
    chats = db.relationship("Chat", backref='community', lazy='dynamic')
