from flask import Blueprint, request, current_app
from typing import cast

from application.modules.user_handling import LoginHandling
from application.api.api_response import ApiResponse
from application.utility.jwt_helper import encode_auth_token

login = Blueprint('login', __name__)
login.url_prefix = '/login'


@login.route('/login', methods=['POST'])
def user_login():

    data:dict = request.get_json()
    user:str = data.get('username', '')
    password:str = data.get('password', '')

    login_handler = cast('LoginHandling', current_app.config['LOGIN_HANDLER'])

    if password == login_handler.read_data_from_user(user=user, parameter='password'):
        
        token = encode_auth_token(user_id=data['username'])
        return ApiResponse.success(message="Login successful", data={'token': token})
    
    else:

        return ApiResponse.error(message="Invalid credentials")
    
@login.route('/logout', methods=['POST'])
def user_logout():

    data:dict = request.get_json()
    user:str = data.get('username', '')

    latest_tokens = current_app.config['ALLOWED_TOKEN']

    if user in latest_tokens:
        del latest_tokens[user]
        current_app.config['ALLOWED_TOKEN'] = {}
        return ApiResponse.success(message="Logout successful")
    else:
        return ApiResponse.error(message="User not logged in")

@login.route('/signup', methods=['POST'])
def user_signup():

    data:dict = request.get_json()
    user:str = data.get('username', '')
    password:str = data.get('password', '')
    reentry_password:str = data.get('reentry_password', '')
    user_level:str = data.get('user_level', '')

    login_handler = cast('LoginHandling', current_app.config['LOGIN_HANDLER'])
    result = login_handler.signup(user=user, password=password, reentry_password=reentry_password, user_level=user_level)

    if result == 'Saved':
        return ApiResponse.success(message="User registered successfully")
    else:
        return ApiResponse.error(message=result)
    
@login.route('/change_password', methods=['POST'])
def change_password():

    data:dict = request.get_json()
    user:str = data.get('username', '')
    old_password:str = data.get('old_password', '')
    new_password:str = data.get('new_password', '')
    reentry_new_password:str = data.get('reentry_new_password', '')

    login_handler = cast('LoginHandling', current_app.config['LOGIN_HANDLER'])
    result = login_handler.change_password(user=user, old_password=old_password, new_password=new_password, reentry_new_password=reentry_new_password)

    if result == 'Saved':
        return ApiResponse.success(message="Password changed successfully")
    else:
        return ApiResponse.error(message=result)
    
@login.route('/delete_user', methods=['POST'])
def delete_user():

    data:dict = request.get_json()
    user:str = data.get('username', '')

    login_handler = cast('LoginHandling', current_app.config['LOGIN_HANDLER'])
    result = login_handler.delete_user(user=user)

    if result == 'User deleted':
        return ApiResponse.success(message="User deleted successfully")
    else:
        return ApiResponse.error(message=result)