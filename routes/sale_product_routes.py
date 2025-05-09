from flask import Blueprint, jsonify, request
from sqlalchemy.exc import IntegrityError
from models.db import db
from models.sale_product import SaleProduct

sale_product = Blueprint('sale_product', __name__)

@sale_product.route('/api/sale_products', methods=['GET'])
def get_sale_products():
    sale_products = SaleProduct.query.all()
    if not sale_products:
        return jsonify({'message': 'No sale_products found'}), 200
    return jsonify([sale_product.serialize() for sale_product in sale_products]), 200

@sale_product.route('/api/add_sale_product', methods=['POST'])
def add_sale_product():
    data = request.get_json()

    if not data or not all(key in data for key in ['price_at_sale', 'quantity', 'subtotal', 'id_sale', 'id_product']):
        return jsonify({'error': 'Missing required data'}), 400
    
    try:
        print(f'Data received: {data}')

        new_sale_product = SaleProduct(
            data['price_at_sale'],
            data['quantity'],
            data['subtotal'],
            data['id_sale'],
            data['id_product'])

        db.session.add(new_sale_product)
        db.session.commit()

        return jsonify({'message': 'SaleProduct successfully added',
                        'sale_product': new_sale_product.serialize()}), 201

    except IntegrityError:
        db.session.rollback()
        return jsonify({'error': 'The sale product is already registered'}), 400

    except Exception as error:
        db.session.rollback()
        print(f'Unexpected error: {error}')
        return jsonify({'error': 'Error adding sale_product'}), 500
    
@sale_product.route('/api/delete_sale_product/<int:id>', methods=['DELETE'])
def del_sale_product(id):
    sale_product = SaleProduct.query.get(id)

    if not sale_product:
        return jsonify({'message': 'SaleProduct not found'}), 404
    
    try:
        db.session.delete(sale_product)
        db.session.commit()
        return jsonify({'message': 'SaleProduct deleted successfully'}), 200
    
    except Exception as error:
        db.session.rollback()
        return jsonify({'error': 'Error deleting sale_product'}), 500
    
@sale_product.route('/api/update_sale_product/<int:id>', methods=['PUT'])
def update_sale_product(id):
    data = request.get_json()

    if not data:
        return jsonify({'error': 'No data received'}, 400)
    
    sale_product = SaleProduct.query.get(id)

    if not sale_product:
        return jsonify({'error': 'SaleProduct not found'}), 404
    
    try:
        sale_product.price_at_sale = data.get('price_at_sale', sale_product.price_at_sale)
        sale_product.quantity = data.get('quantity', sale_product.quantity)
        sale_product.subtotal = data.get('subtotal', sale_product.subtotal)
        sale_product.id_sale = data.get('id_sale', sale_product.id_sale)
        sale_product.id_product = data.get('id_product', sale_product.id_product)

        db.session.commit()

        return jsonify({'message': 'SaleProduct updated successfully',
                        'sale_product': sale_product.serialize()}), 200
    
    except Exception as error:
        db.session.rollback()
        return jsonify({'error': 'Error updating sale_product'}), 500
    
@sale_product.route('/api/patch_sale_product/<int:id>', methods=['PATCH'])
def patch_sale_product(id):
    data = request.get_json()

    if not data:
        return jsonify({'error': 'No data received'}), 400
    
    sale_product = SaleProduct.query.get(id)

    if not sale_product:
        return jsonify({'error': 'SaleProduct not found'}), 404
    
    try:
        if 'price_at_sale' in data:
            sale_product.price_at_sale = data['price_at_sale']
        if 'quantity' in data:
            sale_product.quantity = data['quantity']
        if 'subtotal' in data:
            sale_product.subtotal = data['subtotal']
        if 'id_sale' in data:
            sale_product.id_sale = data['id_sale']
        if 'id_product' in data:
            sale_product.id_product = data['id_product']

        db.session.commit()

        return jsonify({'message': 'SaleProduct patched successfully',
                        'sale_product': sale_product.serialize()}), 200
    
    except Exception as error:
        db.session.rollback()
        return jsonify({'error': 'Error patching sale_product'}), 500