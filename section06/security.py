from werkzeug.security import safe_str_cmp
from models.user import UserModel


def authenticate(username: str, password: str):
    user = UserModel.find_by_username(username)
    return user if user and safe_str_cmp(user.password, password) else None


def identity(payload):
    user_id = payload['identity']
    return UserModel.find_by_id(user_id)
