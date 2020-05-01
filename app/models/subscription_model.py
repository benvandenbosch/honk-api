from app import db
from datetime import datetime, timedelta

"""
This table is used to describe the relationship between a user and the community
they subscribe to. Many to many relationship.
"""
class Subscription(db.Model):

    # Foreign keys (User & Community UUIDs)
    user_uuid = db.Column(db.String(32), db.ForeignKey('user.uuid'), primary_key=True)
    community_uuid = db.Column(db.String(32), db.ForeignKey('community.uuid'), primary_key=True)

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
