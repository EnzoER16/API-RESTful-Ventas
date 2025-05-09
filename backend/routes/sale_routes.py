from flask import Blueprint, jsonify, request
from sqlalchemy.exc import IntegrityError
from models.db import db
from models.sale import Sale
from models.client import Client

sale = Blueprint('sale', __name__)

@sale.route('/api/sales', methods=['GET'])
def get_sales():
    sales = Sale.query.all()
    if not sales:
        return jsonify({'message': 'No sales found'}), 200
    return jsonify([sale.serialize() for sale in sales]), 200

@sale.route('/api/add_sale', methods=['POST'])
def add_sale():
    data = request.get_json()

    if not data or not all(key in data for key in ['date', 'client_id', 'discount', 'amount']):
        return jsonify({'error': 'Missing required data'}), 400
    
    try:
        print(f'Data received: {data}')

        new_sale = Sale(
            data['date'],
            data['client_id'],
            data['discount'],
            data['amount'])

        db.session.add(new_sale)
        db.session.commit()

        return jsonify({'message': 'Sale successfully added',
                        'sale': new_sale.serialize()}), 201

    except IntegrityError:
        db.session.rollback()

    except Exception as error:
        db.session.rollback()
        print(f'Unexpected error: {error}')
        return jsonify({'error': 'Error adding sale'}), 500
    
@sale.route('/api/delete_sale', methods=['DELETE'])
def del_sale():
    sale = Sale.query.get(id)

    if not sale:
        return jsonify({'message': 'Sale not found'}), 404
    
    try:
        db.session.delete(sale)
        db.session.commit()
        return jsonify({'message': 'Sale deleted successfully'}), 200
    
    except Exception as error:
        db.session.rollback()
        return jsonify({'error': 'Error deleting sale'}), 500
    
@sale.route('/api/update_sale', methods=['PUT'])
def update_sale():
    data = request.get_json()

    if not data:
        return jsonify({'error': 'No data received'}, 400)
    
    sale = Sale.query.get(id)

    if not sale:
        return jsonify({'error': 'Sale not found'}), 404
    
    try:
        sale.date = data.get('date', sale.date)
        sale.client_id = data.get('client_id', sale.client_id)
        sale.discount = data.get('discount', sale.discount)
        sale.amount = data.get('amount', sale.amount)

        db.session.commit()

        return jsonify({'message': 'Sale updated successfully',
                        'sale': sale.serialize()}), 200
    
    except Exception as error:
        db.session.rollback()
        return jsonify({'error': 'Error updating sale'}), 500
    
@sale.route('/api/patch_sale', methods=['PATCH'])
def patch_sale():
    data = request.get_json()

    if not data:
        return jsonify({'error': 'No data received'}), 400
    
    sale = Sale.query.get(id)

    if not sale:
        return jsonify({'error': 'Sale not found'}), 404
    
    try:
        if 'date' in data:
            sale.date = data['date']
        if 'client_id' in data:
            sale.client_id = data['client_id']
        if 'discount' in data:
            sale.discount = data['discount']
        if 'amount' in data:
            sale.amount = data['amount']

        db.session.commit()

        return jsonify({'message': 'Sale patched successfully',
                        'sale': sale.serialize()}), 200
    
    except Exception as error:
        db.session.rollback()
        return jsonify({'error': 'Error patching sale'}), 500