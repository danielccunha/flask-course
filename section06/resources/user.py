import sqlite3
from flask_restful import Resource, reqparse

from models.user import UserModel


class UserRegister(Resource):
    @staticmethod
    def __parse_user__():
        parser = reqparse.RequestParser()
        parser.add_argument('username', type=str, required=True)
        parser.add_argument('password', type=str, required=True)
        return parser.parse_args()

    def post(self):
        data = self.__parse_user__()
        if UserModel.find_by_username(data['username']):
            return {"message": "Username is already taken."}, 400

        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        args = (data['username'], data['password'])
        cursor.execute("INSERT INTO users VALUES (NULL, ?, ?)", args)

        connection.commit()
        connection.close()

        return {"message": "User was successfully created."}, 201
