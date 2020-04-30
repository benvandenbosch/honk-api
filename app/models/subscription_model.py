from app import db
from datetime import datetime, timedelta

"""
This table is used to describe the relationship between a user and the community
they subscribe to. Many to many relationship.
"""
class Subscription(db.Model):
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    community_id = db.Column(db.Integer, db.ForeignKey('community.id'), primary_key=True)
    priveleges = db.Column(db.Integer, default=0)

    # Username of person who invited this user to the community
    inviter = db.Column(db.String(64))

    # Creation of subscription
    created_at = db.Column(db.DateTime, default=datetime.utcnow())

    # Binary to check whether subscription is active (1 = active, 0 = inactive)
    is_active = db.Column(db.Integer, default=1)

    # When the subscription is terminated by the user
    terminated_at = db.Column(db.DateTime)

    # Relationship with Community
    community = db.relationship("Community", back_populates="subscriptions")

    # Relationship with User (one to many)
    subscriber = db.relationship("User", back_populates="subscriptions")
