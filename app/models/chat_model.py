from app import db
from datetime import datetime, timedelta
import uuid


class Chat(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    uuid = db.Column(db.String(36), index=True, unique=True)
    community_uuid = db.Column(db.Integer, db.ForeignKey('community.uuid'))
    name = db.Column(db.String(100))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    messages = db.relationship('Message', backref='chat', lazy='dynamic')
    memberships = db.relationship('Membership', back_populates='chat', lazy='dynamic')

    def from_dict(self, data):
        self.name = data['name']
        self.created_at = datetime.utcnow()


    def to_dict(self):
        members = [member.username for member in self.members]
        data = {
            'uuid': self.uuid,
            'name': self.name,
            'created_at': self.created_at,
            'members': members,
            'community': self.community.name if self.community else None
            }

        return data
