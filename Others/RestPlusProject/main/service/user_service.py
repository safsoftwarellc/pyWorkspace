import uuid
import datetime

from main import db
from main.model.user import User


def save_new_user(data):
    user = User.query.filter_by(email=data['email']).first()
    if not user:
        new_user = User(
            public_id = str(uuid.uuid4),
            email = data['email'],
            username = data['username'],
            password = data['password'],
            registered_on = datetime.datetime.utcnow()
        )
        save_changes(new_user)
        return generate_token(new_user)
    else:
        response_object = {
            'status': 'fail',
            'message': 'User Already exists, Please login!'
        }
        return response_object, 409


def get_all_users():
    return User.query.all()

def get_a_user(public_id):
    return User.query.filter_by(public_id=public_id).first()

def save_changes(data):
    db.session.add(data)
    db.session.commit()

def generate_token(user):
    try:
        auth_token = user.encode_auth_token(user.id)
        response_object={
            'status':'Success',
            'message':'Successfully registred',
            'Authorization':auth_token.decode('utf-8')
        }
        return response_object, 201
    except Exception as e:
        response_object={
            'status': 'fail',
            'message':'Some error occured, please try again!'
        }
        return response_object, 401




