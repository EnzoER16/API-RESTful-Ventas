from flask import Blueprint, jsonify, request
from sqlalchemy.exc import IntegrityError
from models.db import db
from models.client import Client

client = Blueprint('client', __name__)

@client.route('/api/clients', methods=['GET'])
def get_clients():
    clients = Client.query.all()
    if not clients:
        return jsonify({'message': 'No clients found'}), 200
    return jsonify([client.serialize() for client in clients]), 200

@client.route('/api/add_client', methods=['POST'])
def add_client():
    data = request.get_json()

    if not data or not all(key in data for key in ['rut', 'name', 'street']):
        return jsonify({'error': 'Missing required data'}), 400
    
    try:
        print(f'Data received: {data}')

        new_client = Client(
            data['rut'],
            data['name'],
            data['street'],
            data.get('number'),
            data.get('district'),
            data.get('city'))

        db.session.add(new_client)
        db.session.commit()

        return jsonify({'message': 'Client successfully added',
                        'client': new_client.serialize()}), 201

    except IntegrityError:
        db.session.rollback()
        return jsonify({'error': 'The client is already registered'}), 400

    except Exception as error:
        db.session.rollback()
        print(f'Unexpected error: {error}')
        return jsonify({'error': 'Error adding client'}), 500
    
@client.route('/api/delete_client/<int:id>', methods=['DELETE'])
def del_client(id):
    client = Client.query.get(id)

    if not client:
        return jsonify({'message': 'Client not found'}), 404
    
    try:
        db.session.delete(client)
        db.session.commit()
        return jsonify({'message': 'Client deleted successfully'}), 200
    
    except Exception as error:
        db.session.rollback()
        return jsonify({'error': 'Error deleting client'}), 500
    
@client.route('/api/update_client/<int:id>', methods=['PUT'])
def update_client(id):
    data = request.get_json()

    if not data:
        return jsonify({'error': 'No data received'}, 400)
    
    client = Client.query.get(id)

    if not client:
        return jsonify({'error': 'Client not found'}), 404
    
    try:
        client.rut = data.get('rut', client.rut)
        client.name = data.get('name', client.name)
        client.street = data.get('street', client.street)
        client.number = data.get('number', client.number)
        client.district = data.get('district', client.district)
        client.city = data.get('city', client.city)

        db.session.commit()

        return jsonify({'message': 'Client updated successfully',
                        'client': client.serialize()}), 200
    
    except Exception as error:
        db.session.rollback()
        return jsonify({'error': 'Error updating client'}), 500
    
@client.route('/api/patch_client/<int:id>', methods=['PATCH'])
def patch_client(id):
    data = request.get_json()

    if not data:
        return jsonify({'error': 'No data received'}), 400
    
    client = Client.query.get(id)

    if not client:
        return jsonify({'error': 'Client not found'}), 404
    
    try:
        if 'rut' in data:
            client.rut = data['rut']
        if 'name' in data:
            client.name = data['name']
        if 'street' in data:
            client.street = data['street']
        if 'number' in data:
            client.number = data['number']
        if 'district' in data:
            client.district = data['district']
        if 'city' in data:
            client.city = data['city']

        db.session.commit()

        return jsonify({'message': 'Client patched successfully',
                        'client': client.serialize()}), 200
    
    except Exception as error:
        db.session.rollback()
        return jsonify({'error': 'Error patching client'}), 500
    
    from flask import jsonify
from models.db import db
from models.client import Client
from models.sale import Sale

@client.route('/api/clients/<int:id_client>/sales', methods=['GET'])
def sales_by_client(id_client):
    client = Client.query.get(id_client)
    if not client:
        return jsonify({'message': 'Cliente no encontrado'}), 404

    sales = Sale.query.filter_by(id_client=id_client).all()

    if not sales:
        return jsonify({'message': 'No sales found for this client'}), 200

    result = [sale.serialize() for sale in sales]

    return jsonify({
        'client': client.serialize(),
        'sales': result
    }), 200