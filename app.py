import datetime
from flask import Flask, jsonify, request


app = Flask(__name__)


ads = {}
id_counter = 1


# POST метод должен создавать объявление
@app.route('/ads', methods=['POST'])
def create_ads():
    global id_counter
    data = request.json or {}
    new_ad = {
        'id': id_counter,
        'title': data.get('title'),
        'description': data.get('description'),
        'created_at': datetime.datetime.now().isoformat(), # Дата создания
        'owner': data.get('owner')
    }
    ads[id_counter] = new_ad
    id_counter += 1
    return jsonify(new_ad), 201


# GET - получать объявление
@app.route('/ads/<int:ad_id>', methods=['GET'])
def get_ad(ad_id):
    if ad_id not in ads:
        return jsonify({'error': 'объявление не найдено'}), 404
    return jsonify(ads[ad_id])

# PATCH - редактировать объявление
@app.route('/ads/<int:ad_id>', methods=['PATCH'])
def update_ad(ad_id):
    if ad_id not in ads:
        return jsonify({'error': 'объявление не найдено'}), 404

    data = request.json or {}
    ad = ads[ad_id]

    
    # редактирование полей
    ad['title'] = data.get('title', ad['title'])
    ad['description'] = data.get('description', ad['description'])
    ad['owner'] = data.get('owner', ad['owner'])

    return jsonify(ad), 200


# DELETE - удалять объявление
@app.route('/ads/<int:ad_id>', methods=['DELETE'])
def delete_ad(ad_id):
    if ad_id not in ads:
        return jsonify({'error': 'объявление не найдено'}), 404
    del ads[ad_id]
    return jsonify({'result': 'объявление успешно удалено'}), 200


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000)

