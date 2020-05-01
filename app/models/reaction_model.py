from app import db
from datetime import datetime, timedelta

"""
This table describes a reaction.
"""

class Reaction(db.Model):

    # ID and UUID within Reaction table
    id = db.Column(db.Integer, primary_key=True)
    uuid = db.Column(db.String(36), index=True, unique=True)

    # Foreign keys with Message & User tables
    author_uuid = db.Column(db.String(32), db.ForeignKey('user.uuid'))
    message_uuid = db.Column(db.String(32), db.ForeignKey('message.uuid'))

    # Record the type of reaction
    reaction_type = db.Column(db.String(20), default="like")

    # Relationship with reaction deliveries
    deliveries = db.relationship('ReactionDelivery', back_populates='reaction', lazy='dynamic')
