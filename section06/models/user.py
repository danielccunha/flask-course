import sqlite3


class UserModel:
    def __init__(self, _id: int, username: str, password: str):
        self.id = _id
        self.username = username
        self.password = password

    @classmethod
    def find_by_username(cls, username: str):
        connection = sqlite3.connect("data.db")
        cursor = connection.cursor()

        query = "SELECT * FROM users WHERE username=?"
        result = cursor.execute(query, (username,))
        row = result.fetchone()
        user = UserModel(*row) if row else None

        connection.close()
        return user

    @classmethod
    def find_by_id(cls, id: int):
        connection = sqlite3.connect("data.db")
        cursor = connection.cursor()

        query = "SELECT * FROM users WHERE id=?"
        result = cursor.execute(query, (id,))
        row = result.fetchone()
        user = UserModel(*row) if row else None

        connection.close()
        return user
