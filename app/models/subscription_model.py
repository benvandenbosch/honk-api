from app import db
from datetime import datetime, timedelta

"""
This table is used to describe the relationship between a user and the community
they subscribe to. Many to many relationship.
"""
class Subscription(db.Model):

    # ID
    id = db.Column(db.Integer, primary_key=True, unique=True, index=True)

    # Foreign keys and foreign uuids
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    community_id = db.Column(db.Integer, db.ForeignKey('community.id'))
    user_uuid = db.Column(db.String(32))
    community_uuid = db.Column(db.String(32))

    # Track user priveleges (0 = standard user, 1 = admin)
    priveleges = db.Column(db.Integer, default=0)

    # Track validity timeframes for this Subscription
    created_at = db.Column(db.DateTime, default=datetime.utcnow())
    deactivated_at = db.Column(db.DateTime)
    is_active = db.Column(db.Boolean, default=True)

    # Track who added the person to the chat (username)
    inviter = db.Column(db.String(64))

    # Relationships with Community and User
    community = db.relationship('Community', back_populates='subscriptions')
    subscriber = db.relationship('User', back_populates='subscriptions')
