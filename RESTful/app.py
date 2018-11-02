from flask import Flask
from flask_restful import Resource, Api, request

app = Flask(__name__)
api = Api(app)

items = []

class Item(Resource):
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
        data = request.get_json(force=True)
        price = data['price']
        for item in items:
            if item['name'] == name:
                item['price'] = price
                return item
        new_item = {'name': name, 'price': price}
        items.append(new_item)
        return new_item

class ItemList(Resource):
    def get(self):
        return {'items': items}




api.add_resource(Item, '/item/<string:name>') 
api.add_resource(ItemList, '/items')

app.run(port=5000, debug=True)


        

