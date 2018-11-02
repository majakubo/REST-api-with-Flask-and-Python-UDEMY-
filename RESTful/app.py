from flask import Flask
from flask_restful import Resource, Api, request, reqparse
from flask_jwt import JWT, jwt_required
from security import authentication, identity

app = Flask(__name__)
app.secret_key = 'super_super_secret_key'
api = Api(app)

jwt = JWT(app, authentication, identity)

items = []

class Item(Resource):
    @jwt_required()
    def get(self, name):
        # instead using list(filter()) we use next(filter()) to get first item from filter
        item = next(filter(lambda x: x['name'] == name, items), None)
        return {'item': item}, 200 if item else 404
    
    
    def post(self, name):
        if next(filter(lambda x: x['name'] == name, items), None) is not None:
            return {'message': "an item with name '{}' already exists.".format(name)}, 400

        data = request.get_json(force=True)
        item = {'name': name, 'price': data['price']}
        items.append(item)
        return item, 200
    
    
    def put(self, name):
        parser = reqparse.RequestParser()
        parser.add_argument('price',
                type=float,
                required=True,
                help="This field cannot be left blank!"
        )
        data = parser.parse_args()

        item = next(filter(lambda x: x['name'] == name, items), None)
        if item is None:
            item = {'name': name, 'price': data['price']}
            items.append(item)
        else:
            item.update(data)

        return item
    
    def delete(self, name):
        global items
        items = list(filter(lambda x: x['name'] != name, items))

class ItemList(Resource):
    def get(self):
        return {'items': items}




api.add_resource(Item, '/item/<string:name>') 
api.add_resource(ItemList, '/items')

app.run(port=5000, debug=True)


        

