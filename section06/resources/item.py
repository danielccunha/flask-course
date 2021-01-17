import sqlite3
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required

from models.item import ItemModel


class Item(Resource):
    @classmethod
    def __parse_item__(cls):
        parser = reqparse.RequestParser()
        parser.add_argument('price', type=float, required=True, help='This field cannot be left blank!')
        return parser.parse_args()

    @jwt_required()
    def get(self, name: str):
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()
        return {'message': 'Item not found.'}, 404

    @jwt_required()
    def post(self, name):
        if ItemModel.find_by_name(name):
            return {'message': f'An item with name "{name}" already exists.'}, 400
        data = self.__parse_item__()
        item = ItemModel(name, data['price'])

        try:
            item.insert()
        except sqlite3.Error:
            return {"message": "An error occurred inserting the item."}, 500

        return item.json(), 201

    @classmethod
    @jwt_required()
    def delete(cls, name: str):
        ItemModel.delete(name)
        return None, 204

    @jwt_required()
    def put(self, name):
        data = self.__parse_item__()
        item = ItemModel.find_by_name(name)
        updated_item = ItemModel(name, data['price'])

        if item is None:
            updated_item.insert()
        else:
            updated_item.update()

        return updated_item.json()


class ItemList(Resource):
    @jwt_required()
    def get(self):
        items = ItemModel.find_all()
        return [item.json() for item in items]
