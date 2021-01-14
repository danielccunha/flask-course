from flask import Flask, request
from flask_restful import Resource, Api, reqparse
from flask_jwt import JWT, jwt_required

from security import authenticate, identity

app = Flask(__name__)
app.secret_key = 'development'
api = Api(app)

jwt = JWT(app, authenticate, identity)

items = []


class Item(Resource):
    @staticmethod
    def __find_item__(name):
        return next(filter(lambda item: item['name'] == name, items), None)

    @staticmethod
    def __parse_item__():
        parser = reqparse.RequestParser()
        parser.add_argument('price', type=float, required=True, help='This field cannot be left blank!')
        return parser.parse_args()

    @jwt_required()
    def get(self, name):
        found_item = self.__find_item__(name)
        if found_item is None:
            return {'error': 'Item not found.'}, 404
        return found_item

    @jwt_required()
    def post(self, name):
        if self.__find_item__(name):
            return {'message': f'An item with name "{name}" already exists.'}, 400
        data = self.__parse_item__()
        item = {'name': name, 'price': data['price']}
        items.append(item)
        return item, 201

    @staticmethod
    @jwt_required()
    def delete(name):
        global items
        items = list(filter(lambda item: item['name'] != name, items))
        return None, 204

    @jwt_required()
    def put(self, name):
        data = self.__parse_item__()
        item = self.__find_item__(name)

        if item is None:
            item = {'name': name, 'price': data['price']}
            items.append(item)
        else:
            item.update(data)

        return item


class ItemList(Resource):
    @jwt_required()
    def get(self):
        return items


api.add_resource(Item, '/items/<string:name>')
api.add_resource(ItemList, '/items')

app.run(debug=True)
