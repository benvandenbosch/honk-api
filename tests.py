#!/usr/bin/env python

from config import Config
from datetime import datetime, timedelta
import unittest
from app import create_app, db
from app.models.user_model import User
from app.models.message_model import Message
from app.models.chat_model import Chat
from app.models.community_model import Community
from config import Config
from flask import jsonify
from flask_testing import TestCase
import json
import base64
from requests.auth import _basic_auth_str
import uuid

def get_token(username, password):
    """
    Utility function for getting auth tokens without repeating API call in
    every test
    """
    header = {"Authorization": _basic_auth_str(username, password)}
    response = self.client.post('/api/tokens', headers=header)
    return response.json['token']


# Create subclass to override SQLAlchemy config and make in-memory SQLite db
class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite://'


class UserModelCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app(TestConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_password_hashing(self):
        u = User(username='susan', uuid=uuid.uuid4().hex)
        u.set_password('cat')
        self.assertFalse(u.check_password('dog'))
        self.assertTrue(u.check_password('cat'))

    def test_join_chat(self):
        u = User(username='test', email='test@email.com', uuid=uuid.uuid4().hex)
        u2 = User(username='test2', email='test2@gmail.com', uuid=uuid.uuid4().hex)
        db.session.add(u)
        db.session.add(u2)
        db.session.commit()

        c = Chat(name='chat1', uuid=uuid.uuid4().hex)
        db.session.add(c)
        db.session.commit()

        u.join_chat(c)
        u2.join_chat(c)
        db.session.commit()

        self.assertEqual(len(c.members), 2)
        self.assertTrue(u in c.members)
        self.assertTrue(u2 in c.members)

class UserSignupFlow(TestCase):

    def create_app(self):
        return create_app(TestConfig)

    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    # Test that a user can be created and proper response is returned
    def test_create_user(self):
        header = {"Content-Type": "application/json"}
        payload = json.dumps({
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'testpassword'
        })


        # Create the user
        response = self.client.post('/api/users', headers=header, data=payload)
        expected_response = User.query.filter_by(username='testuser').first().to_dict()

        # Response status code should be 201 for successful creation
        self.assertEqual(201, response.status_code)

        # Assert that response is equal to database entry
        self.assertEqual(expected_response, response.json)

    def test_create_token(self):
        header = {"Content-Type": "application/json"}
        payload = json.dumps({
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'testpassword'
        })
        self.client.post('/api/users', headers=header, data=payload)


        # Test that a registered user can get a token
        header = {"Authorization": _basic_auth_str('testuser', 'testpassword')}
        response = self.client.post('/api/tokens', headers=header)

        self.assertTrue(response.status_code == 200)

        # Test that the token works at a token-guarded endpoint
        token = response.json['token']
        header = {'Authorization': ('Bearer ' + token)}
        response = self.client.get('api/users/' + str(1), headers=header)

        self.assertTrue(response.json['username'] == 'testuser')
        self.assertTrue(response.status_code == 200)

class MessageOps(TestCase):

    def create_app(self):
        return create_app(TestConfig)

    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    # Test that a user can be created and proper response is returned
    def test_create_chat(self):

        # Create three test users
        user_one = User(username='testuser1',email='test1@test.com', uuid=uuid.uuid4().hex)
        user_one.set_password('testpass')
        user_one.get_token()

        user_two = User(username='testuser2',email='test2@test.com', uuid=uuid.uuid4().hex)
        user_two.set_password('testpass2')
        user_two.get_token()

        user_three = User(username='testuser3',email='test3@test.com', uuid=uuid.uuid4().hex)
        user_three.set_password('testpass3')
        user_three.get_token()

        db.session.commit()

        # Create a chat with another user
        header = {'Authorization': 'Bearer ' + user_one.token,
                  "Content-Type": "application/json"}
        payload = json.dumps({
            'name': 'testchat1',
            'members': [
                'testuser2'
            ]
        })
        response = self.client.post('/api/chats', headers=header, data=payload)
        self.assertEqual(response.status_code, 201)
        self.assertTrue(response.json['name'] == 'testchat1')
        self.assertTrue(response.json['members'] == ['testuser1', 'testuser2'])

        chat1_id = response.json['id']

        # Test that an error is not thrown if a user already in the chat is added
        payload = json.dumps({
            'username': 'testuser1'
        })
        response = self.client.put('/api/chats/invite/' + str(chat1_id), headers=header, data=payload)
        self.assertEqual(response.status_code, 201)
        self.assertTrue(response.json['members'] == ['testuser1', 'testuser2'])


        # Test that another user cannot join the chat without being added
        header = {'Authorization': 'Bearer ' + user_three.token,
                  "Content-Type": "application/json"}
        payload = json.dumps({
            'username': 'testuser3'
        })
        response = self.client.put(('/api/chats/invite/' + str(chat1_id)), headers=header, data=payload)
        self.assertEqual(response.status_code, 400)

        # Test that a user can be successfully added by current chat member
        header = {'Authorization': 'Bearer ' + user_one.token,
                  "Content-Type": "application/json"}
        payload = json.dumps({
         'username': 'testuser3'
        })
        response = self.client.put(('/api/chats/invite/' + str(chat1_id)), headers=header, data=payload)
        self.assertEqual(response.status_code, 201)
        self.assertTrue(response.json['members'] == ['testuser1', 'testuser2', 'testuser3'])


    def test_messenger(self):
        # Create three test users
        user_one = User(username='testuser1',email='test1@test.com', uuid=uuid.uuid4().hex)
        user_one.set_password('testpass')
        user_one.get_token()

        user_two = User(username='testuser2',email='test2@test.com', uuid=uuid.uuid4().hex)
        user_two.set_password('testpass2')
        user_two.get_token()

        user_three = User(username='testuser3',email='test3@test.com', uuid=uuid.uuid4().hex)
        user_three.set_password('testpass3')
        user_three.get_token()

        # Create test chats
        chat_one = Chat(name='chat1', created_at=datetime.utcnow(), uuid=uuid.uuid4().hex)
        chat_one.members.append(user_one)
        chat_one.members.append(user_two)
        chat_one.members.append(user_three)


        chat_two = Chat(name='chat2', created_at=datetime.utcnow(), uuid=uuid.uuid4().hex)
        chat_two.members.append(user_one)
        chat_two.members.append(user_two)

        chat_three = Chat(name='chat3', created_at=datetime.utcnow(), uuid=uuid.uuid4().hex)
        chat_three.members.append(user_two)
        chat_three.members.append(user_three)

        db.session.commit()
        # Sent two consecutive messages from user 1 in chat 1
        header = {'Authorization': 'Bearer ' + user_one.token,
                'Content-Type': 'application/json'}
        payload = json.dumps({
            'chat_id': chat_one.id,
            'content': "hey two and three, it is me one"
        })
        response = self.client.post('/api/messages', headers=header, data=payload)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json['author'], 'testuser1')
        self.assertEqual(response.json['content'], "hey two and three, it is me one")
        self.assertEqual(response.json['chat'], chat_one.name)

        payload = json.dumps({
            'chat_id': chat_one.id,
            'content': "can you guys hear me?"
        })
        response = self.client.post('/api/messages', headers=header, data=payload)
        self.assertEqual(response.status_code, 201)

        # Add a message from user 3
        header = {'Authorization': 'Bearer ' + user_three.token,
                'Content-Type': 'application/json'}
        payload = json.dumps({
            'chat_id': chat_one.id,
            'content': "It's me three! yes I can hear you"
        })
        response = self.client.post('/api/messages', headers=header, data=payload)
        self.assertEqual(response.status_code, 201)

        # Add a message from user 2
        header = {'Authorization': 'Bearer ' + user_two.token,
            'Content-Type': 'application/json'}
        payload = json.dumps({
            'chat_id': chat_one.id,
            'content': "I'm here too!"
        })
        response = self.client.post('/api/messages', headers=header, data=payload)
        self.assertEqual(response.status_code, 201)

        # Test that messages are loaded properly with get
        response = self.client.get('/api/messages/' + str(chat_one.id), headers=header)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json), 4)
        self.assertEqual(response.json[0]['author'], 'testuser2')
        self.assertEqual(response.json[0]['content'], "I'm here too!")
        self.assertEqual(response.json[3]['author'], 'testuser1')
        self.assertEqual(response.json[3]['content'], "hey two and three, it is me one")

        # Start messaging in chat 2
        payload = json.dumps({
            'chat_id': chat_two.id,
            'content': "hey one, we're in this chat without 3"
        })
        response = self.client.post('api/messages', headers=header, data=payload)
        self.assertEqual(response.status_code, 201)

        # user 1 send a message in chat 2
        header = {'Authorization': 'Bearer ' + user_one.token,
            'Content-Type': 'application/json'}
        payload = json.dumps({
            'chat_id': chat_two.id,
            'content': "ha, yeah, unless we add him to it"
        })
        response = self.client.post('api/messages', headers=header, data=payload)
        self.assertEqual(response.status_code, 201)

        # Test that 3 can't access things in chat 2
        header = {'Authorization': 'Bearer ' + user_three.token,
            'Content-Type': 'application/json'}
        response = self.client.get('api/messages/' + str(chat_two.id), headers=header)
        self.assertEqual(response.status_code, 400)

        # Add 3 to chat 2 (simulates getting added)
        user_three.join_chat(chat_two)
        response = self.client.get('api/messages/' + str(chat_two.id), headers=header)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json), 2)
        self.assertEqual(response.json[0]['content'], "ha, yeah, unless we add him to it")
        self.assertEqual(response.json[1]['content'], "hey one, we're in this chat without 3")

class Communities(TestCase):

    def create_app(self):
        return create_app(TestConfig)

    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_unit_community(self):
        # Create three test users
        user_one = User(username='testuser1',email='test1@test.com', uuid=uuid.uuid4().hex)
        user_one.set_password('testpass')
        user_one.get_token()

        db.session.commit()

        # Create a chat with another user
        header = {'Authorization': 'Bearer ' + user_one.token,
                  "Content-Type": "application/json"}
        payload = json.dumps({
            'name': 'community1',
            'description': 'a place for hanging out'
        })
        response = self.client.post('/api/communities', headers=header, data=payload)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json['name'], 'community1')
        self.assertEqual(response.json['description'], 'a place for hanging out')
        self.assertEqual(response.json['admins'], ['testuser1'])
        self.assertEqual(response.json['subscribers'], ['testuser1'])

        # Test adding a user to a community
        user_two = User(username='testuser2', email='test2@test.com', uuid=uuid.uuid4().hex)
        db.session.add(user_two)
        db.session.commit()
        payload = json.dumps({
            'username': 'testuser2',
            'community_name': 'community1'
        })
        response = self.client.put('/api/communities/invite', headers=header, data=payload)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json['subscribers'], ['testuser1', 'testuser2'])

    def test_add_chat_to_community(self):
        # Create three test users
        user_one = User(username='testuser1',email='test1@test.com')
        user_one.set_password('testpass')
        user_one.get_token()

        db.session.commit()

        # Create a chat with another user
        header = {'Authorization': 'Bearer ' + user_one.token,
                  "Content-Type": "application/json"}
        payload = json.dumps({
            'name': 'community1',
            'description': 'a place for hanging out'
        })
        response = self.client.post('/api/communities', headers=header, data=payload)
        self.assertEqual(response.status_code, 201)

        # Create a chat within the community
        payload = json.dumps({
            'name': 'chat1incomm1',
            'members': [],
            'community_name': 'community1'
        })
        response = self.client.post('/api/chats', headers=header, data=payload)
        self.assertEqual(response.status_code, 201)

        community = Community.query.first()
        self.assertEqual(community.to_dict()['chats'], ['chat1incomm1'])


if __name__ == '__main__':
    unittest.main()
