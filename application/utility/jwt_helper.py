import jwt
from datetime import datetime, timedelta, timezone
from functools import wraps
from flask import request, jsonify
from flask import current_app

def encode_auth_token(user_id):

    secret_key = current_app.config['SECRET_KEY']

    payload = {
        'exp': str(datetime.now(timezone.utc) + timedelta(hours=1)),
        'iat': str(datetime.now(timezone.utc)),
        'sub': user_id
    }

    token = jwt.encode(payload, secret_key, algorithm='HS256')

    current_app.config['ALLOWED_TOKEN'][user_id] = token

    return token

def decode_auth_token(auth_token):

    secret_key = current_app.config['SECRET_KEY']

    try:
        payload = jwt.decode(auth_token, secret_key, algorithms=['HS256'])
        return payload['sub']
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None
    

#TODO This is garbage implement a proper way

def jwt_required(f):
    
    @wraps(f)
    def decorated(*args, **kwargs):
        auth_header = request.headers.get('Authorization', '')
        token = auth_header.replace('Bearer ', '')
        latest_tokens = current_app.config['ALLOWED_TOKEN']

        if not token:
            return jsonify({'msg': 'Missing token'}), 401
        user_id = decode_auth_token(token)
        if not user_id:
            return jsonify({'msg': 'Invalid or expired token'}), 401
        if latest_tokens.get(user_id) != token:
            return jsonify({'msg': 'Token is not the latest or is invalid'}), 401
        return f(*args, **kwargs)
    return decorated