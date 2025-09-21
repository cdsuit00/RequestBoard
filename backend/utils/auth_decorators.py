from functools import wraps
from flask import request, jsonify, current_app
import jwt
from models import User
from extensions import db

def get_current_user_from_request():
    auth_header = request.headers.get('Authorization', '')
    if not auth_header:
        return None, {'error': 'Missing Authorization header'}
    if not auth_header.startswith('Bearer '):
        return None, {'error': 'Invalid Authorization header format'}
    token = auth_header.split(' ', 1)[1]
    try:
        payload = jwt.decode(token, current_app.config['JWT_SECRET_KEY'], algorithms=['HS256'])
        user = User.query.get(payload.get('user_id'))
        if not user:
            return None, {'error': 'User not found'}
        return user, None
    except jwt.ExpiredSignatureError:
        return None, {'error': 'Token expired'}
    except jwt.InvalidTokenError:
        return None, {'error': 'Invalid token'}
    except Exception as e:
        return None, {'error': 'Auth error'}

def login_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        user, err = get_current_user_from_request()
        if err:
            return jsonify(err), 401
        return f(user, *args, **kwargs)
    return wrapper
