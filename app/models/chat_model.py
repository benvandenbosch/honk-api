from app import db
from datetime import datetime, timedelta
import uuid


class Chat(db.Model):

    # ID & UUID
    id = db.Column(db.Integer, primary_key=True)
    uuid = db.Column(db.String(36), index=True, unique=True)

    # Foreign key for parent community
    community_uuid = db.Column(db.Integer, db.ForeignKey('community.uuid'))

    # Chat profile
    name = db.Column(db.String(100))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    messages = db.relationship('Message', backref='chat', lazy='dynamic')
    memberships = db.relationship('Membership', back_populates='chat', lazy='dynamic')

    def from_dict(self, data):
        self.name = data['name']
        self.created_at = datetime.utcnow()
        self.uuid = uuid.uuid4().hex


    def to_dict(self):
        data = {
            'uuid': self.uuid,
            'name': self.name,
            'created_at': self.created_at,
            'members': [membership.member.uuid for membership in self.memberships],
            'community': self.community_uuid if self.community else None,
            'messages': [message.to_dict() for message in self.messages]
            }

        return data
