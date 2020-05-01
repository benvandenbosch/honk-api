from app import db
from datetime import datetime, timedelta

"""
This table describes the relationship between a reaction and its recipients. It
is a many to many table.
"""

class ReactionDelivery(db.Model):

    # Foreign keys with User and Reaction tables
    recipient_uuid = db.Column(db.String(32), db.ForeignKey('user.uuid'), primary_key=True)
    reaction_uuid = db.Column(db.String(32), db.ForeignKey('reaction.uuid'), primary_key=True)

    # Track whether reaction has been successfully delivered
    is_delivered = db.Column(db.Boolean, default=False)

    # Relationship with user
    recipient = db.relationship("User", back_populates="reaction_deliveries")

    # Relationship with reaction
    message = db.relatinoship("Reaction", back_populates="deliveries")
