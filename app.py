from flask import Flask, jsonify, request

app = Flask(__name__)
stores = [
        {
            'name': 'My wonderful Store',
            'items': [
                {
                    'name': 'My item',
                    'price': 15.99
                }
        
            ]
        }
]
# POST - used to recive data
# GET - used to send data back only


# POST   /store data: {name;}
@app.route('/store', methods=['POST'])
def create_store():
    request_data = request.get_json()
    new_store = {
            'name': request_data['name'],
            'items': []    
    }
    stores.append(new_store)

    return jsonify(new_store)


# GET    /store/<string:name>
@app.route('/store/<string:name>') # http://127.0.0.1:5000/store/some_name
def get_store(name):
    # iterate over stores
    # if the store name matches, return it
    # if none match, return an error message

    for store in stores:
        if store['name'] == name:
            return jsonify(store)

    return jsonify({'message': 'store not found'})



# GET    /store
@app.route('/store')
def get_stores(): 
    return jsonify({'stores': stores})


# POST   /store/<string:name>/item {name;, price;}
@app.route('/store/<string:name>/item', methods=['POST'])
def create_item_in_store(name):
    request_data = request.get_json()
    for store in stores:
        if store['name'] == name:
            new_item = {
                    'name': request_data['name']
                    'price': request_data['price']
            }
            return jsonify(new_item)
    return jsonify({'message': 'store not found'})


# GET    /store/<string:name>/item
@app.route('/store/<string:name>/item')
def get_item_in_store(name):
    for store in sotres:
        if store['name'] == name:
            return jsonify({'items': store['items']})

    return jsonify{'message': 'no such item in store'}


app.run(port=5000, debug=True)

