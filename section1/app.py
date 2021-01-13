from flask import Flask, jsonify, request, render_template

app = Flask(__name__)
stores = []


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/stores', methods=['POST'])
def create_store():
    request_data = request.get_json()
    stores.append({'name': request_data['name'], 'items': []})
    return jsonify(stores[-1])


@app.route('/stores/<string:name>')
def get_store(name: str):
    found_store = next(filter(lambda store: store['name'] == name, stores), None)
    return jsonify({'error': 'Store not found.'}) if found_store is None else jsonify(found_store)


@app.route('/stores')
def get_stores():
    return jsonify(stores)


@app.route('/stores/<string:name>/items', methods=['POST'])
def create_item_in_store(name: str):
    request_data = request.get_json()

    for store in stores:
        if store['name'] == name:
            item = {'name': request_data['name'], 'price': request_data['price']}
            store['items'].append(item)
            return jsonify(item)

    return jsonify({'error': 'Store not found.'})


@app.route('/stores/<string:name>/items')
def get_items_in_store(name: str):
    found_store = next(filter(lambda store: store['name'] == name, stores), None)
    return jsonify({'error': 'Store not found.'}) if found_store is None else jsonify(found_store['items'])


app.run()
