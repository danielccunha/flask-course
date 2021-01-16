import sqlite3
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required


class Item(Resource):
    @staticmethod
    def __find_by_name__(name: str):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT * FROM items WHERE name=?"
        result = cursor.execute(query, (name,))
        row = result.fetchone()
        connection.close()

        return {'name': row[0], 'price': row[1]} if row else None

    @staticmethod
    def __parse_item__():
        parser = reqparse.RequestParser()
        parser.add_argument('price', type=float, required=True, help='This field cannot be left blank!')
        return parser.parse_args()

    @jwt_required()
    def get(self, name):
        user = self.__find_by_name__(name)
        if user:
            return user
        return {'message': 'Item not found.'}, 404

    @jwt_required()
    def post(self, name):
        if self.__find_by_name__(name):
            return {'message': f'An item with name "{name}" already exists.'}, 400
        data = self.__parse_item__()
        item = {'name': name, 'price': data['price']}

        try:
            self.__insert_item__(item)
        except sqlite3.Error:
            return {"message": "An error occurred inserting the item."}, 500

        return item, 201

    @staticmethod
    def __insert_item__(item):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "INSERT INTO items VALUES (?, ?)"
        cursor.execute(query, (item['name'], item['price']))

        connection.commit()
        connection.close()

    @staticmethod
    @jwt_required()
    def delete(name):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "DELETE FROM items WHERE name=?"
        cursor.execute(query, (name,))

        connection.commit()
        connection.close()

        return None, 204

    @jwt_required()
    def put(self, name):
        data = self.__parse_item__()
        item = self.__find_by_name__(name)
        updated_item = {'name': name, 'price': data['price']}

        if item is None:
            self.__insert_item__(updated_item)
        else:
            self.__update_item__(updated_item)

        return updated_item

    @staticmethod
    def __update_item__(item):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "UPDATE items SET PRICE=? WHERE name=?"
        cursor.execute(query, (item['price'], item['name']))

        connection.commit()
        connection.close()


class ItemList(Resource):
    @jwt_required()
    def get(self):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT * FROM items"
        result = cursor.execute(query)
        rows = result.fetchall()

        return [{'name': row[0], 'price': row[1]} for row in rows]
