from flask import Blueprint, jsonify, request
from sqlalchemy.exc import IntegrityError
from models.db import db
from models.sale import Sale
from models.client import Client
from models.product import Product
from models.sale_product import SaleProduct

sale = Blueprint('sale', __name__)
sale_routes = Blueprint('sale_routes', __name__)

@sale.route('/api/sales', methods=['GET'])
def get_sales():
    sales = Sale.query.all()
    if not sales:
        return jsonify({'message': 'No sales found'}), 200
    return jsonify([sale.serialize() for sale in sales]), 200

@sale.route('/api/add_sale', methods=['POST'])
def add_sale():
    data = request.get_json()

    if not data or not all(key in data for key in ['date', 'discount', 'amount', 'id_client']):
        return jsonify({'error': 'Missing required data'}), 400
    
    try:
        print(f'Data received: {data}')

        new_sale = Sale(
            data['date'],
            data['discount'],
            data['amount'],
            data['id_client'])

        db.session.add(new_sale)
        db.session.commit()

        return jsonify({'message': 'Sale successfully added',
                        'sale': new_sale.serialize()}), 201

    except IntegrityError:
        db.session.rollback()
        return jsonify({'error': 'The sale is already registered'}), 400

    except Exception as error:
        db.session.rollback()
        print(f'Unexpected error: {error}')
        return jsonify({'error': 'Error adding sale'}), 500
    
@sale.route('/api/delete_sale/<int:id>', methods=['DELETE'])
def del_sale(id):
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
    
@sale.route('/api/update_sale/<int:id>', methods=['PUT'])
def update_sale(id):
    data = request.get_json()

    if not data:
        return jsonify({'error': 'No data received'}, 400)
    
    sale = Sale.query.get(id)

    if not sale:
        return jsonify({'error': 'Sale not found'}), 404
    
    try:
        sale.date = data.get('date', sale.date)
        sale.discount = data.get('discount', sale.discount)
        sale.amount = data.get('amount', sale.amount)
        sale.client_id = data.get('client_id', sale.client_id)

        db.session.commit()

        return jsonify({'message': 'Sale updated successfully',
                        'sale': sale.serialize()}), 200
    
    except Exception as error:
        db.session.rollback()
        return jsonify({'error': 'Error updating sale'}), 500
    
@sale.route('/api/patch_sale/<int:id>', methods=['PATCH'])
def patch_sale(id):
    data = request.get_json()

    if not data:
        return jsonify({'error': 'No data received'}), 400
    
    sale = Sale.query.get(id)

    if not sale:
        return jsonify({'error': 'Sale not found'}), 404
    
    try:
        if 'date' in data:
            sale.date = data['date']
        if 'discount' in data:
            sale.discount = data['discount']
        if 'amount' in data:
            sale.amount = data['amount']
        if 'client_id' in data:
            sale.client_id = data['client_id']

        db.session.commit()

        return jsonify({'message': 'Sale patched successfully',
                        'sale': sale.serialize()}), 200
    
    except Exception as error:
        db.session.rollback()
        return jsonify({'error': 'Error patching sale'}), 500
    
@sale_routes.route('/api/sales-history', methods=['GET'])
def sales_history():
    sales = Sale.query.all()
    history = []

    for sale in sales:
        sale_products = SaleProduct.query.filter_by(id_sale=sale.id_sale).all()
        product_details = []

        for sp in sale_products:
            product = Product.query.get(sp.id_product)
            product_details.append({
                'product_name': product.name,
                'quantity': sp.quantity,
                'price_at_sale': sp.price_at_sale,
                'subtotal': sp.subtotal
            })

        history.append({
            'id_sale': sale.id_sale,
            'date': sale.date.strftime('%Y-%m-%d'),
            'discount': sale.discount,
            'amount': sale.amount,
            'products': product_details
        })

    return jsonify(history), 200
