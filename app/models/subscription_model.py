from app import db
from datetime import datetime, timedelta

"""
This table is used to describe the relationship between a user and the community
they subscribe to.
"""
class Subscription(db.Model):
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    community_id = db.Column(db.Integer, db.ForeignKey('community.id'), primary_key=True)
    priveleges = db.Column(db.Integer)

    # Relationship with Community
    community = db.relationship("Community", back_populates="subscriptions")

    # Relationship with User
    user = db.relationship("User", back_populates="subscriptions")
