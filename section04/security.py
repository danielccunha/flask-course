from werkzeug.security import safe_str_cmp
from user import User

users = [User(1, 'daniel', '123')]
username_mapping = {user.username: user for user in users}
userid_mapping = {user.id: user for user in users}


def authenticate(username: str, password: str):
    user = username_mapping.get(username, None)
    return user if user and safe_str_cmp(user.password, password) else None


def identity(payload):
    user_id = payload['identity']
    return userid_mapping.get(user_id, None)
