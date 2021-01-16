import sqlite3
from flask_restful import Resource, reqparse


class User:
    def __init__(self, _id: int, username: str, password: str):
        self.id = _id
        self.username = username
        self.password = password

    @staticmethod
    def find_by_username(username: str):
        connection = sqlite3.connect("data.db")
        cursor = connection.cursor()

        query = "SELECT * FROM users WHERE username=?"
        result = cursor.execute(query, (username,))
        row = result.fetchone()
        user = User(*row) if row else None

        connection.close()
        return user

    @staticmethod
    def find_by_id(id: int):
        connection = sqlite3.connect("data.db")
        cursor = connection.cursor()

        query = "SELECT * FROM users WHERE id=?"
        result = cursor.execute(query, (id,))
        row = result.fetchone()
        user = User(*row) if row else None

        connection.close()
        return user


class UserRegister(Resource):
    @staticmethod
    def __parse_user__():
        parser = reqparse.RequestParser()
        parser.add_argument('username', type=str, required=True)
        parser.add_argument('password', type=str, required=True)
        return parser.parse_args()

    def post(self):
        data = self.__parse_user__()
        if User.find_by_username(data['username']):
            return {"message": "Username is already taken."}, 400

        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        args = (data['username'], data['password'])
        cursor.execute("INSERT INTO users VALUES (NULL, ?, ?)", args)

        connection.commit()
        connection.close()

        return {"message": "User was successfully created."}, 201
