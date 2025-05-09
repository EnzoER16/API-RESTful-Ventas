from flask import Blueprint, jsonify, request
from sqlalchemy.exc import IntegrityError
from models.db import db
from models.phone import Phone
from models.sale import Sale
from datetime import datetime, timedelta

phone = Blueprint('phone', __name__)


@phone.route('/api/phones', methods=['GET'])
def get_phones():
    phones = Phone.query.all()
    if not phones:
        return jsonify({'message': 'No phones found'}), 200
    return jsonify([phone.serialize() for phone in phones]), 200


@phone.route('/api/add_phone', methods=['POST'])
def add_phone():
    data = request.get_json()

    if not data or not all(key in data for key in ['phone', 'id_client']):
        return jsonify({'error': 'Missing required data'}), 400

    try:
        print(f'Data received: {data}')

        new_phone = Phone(
            data['phone'],
            data['id_client'])

        db.session.add(new_phone)
        db.session.commit()

        return jsonify({'message': 'Phone successfully added',
                        'phone': new_phone.serialize()}), 201

    except IntegrityError:
        db.session.rollback()
        return jsonify({'error': 'The phone is already registered'}), 400

    except Exception as error:
        db.session.rollback()
        print(f'Unexpected error: {error}')
        return jsonify({'error': 'Error adding phone'}), 500


@phone.route('/api/delete_phone/<int:id>', methods=['DELETE'])
def del_phone(id):
    phone = Phone.query.get(id)

    if not phone:
        return jsonify({'message': 'Phone not found'}), 404

    try:
        db.session.delete(phone)
        db.session.commit()
        return jsonify({'message': 'Phone deleted successfully'}), 200

    except Exception as error:
        db.session.rollback()
        return jsonify({'error': 'Error deleting phone'}), 500


@phone.route('/api/update_phone/<int:id>', methods=['PUT'])
def update_phone(id):
    data = request.get_json()

    if not data:
        return jsonify({'error': 'No data received'}, 400)

    phone = Phone.query.get(id)

    if not phone:
        return jsonify({'error': 'Phone not found'}), 404

    try:
        phone.phone = data.get('phone', phone.phone)
        phone.id_client = data.get('id_client', phone.id_client)

        db.session.commit()

        return jsonify({'message': 'Phone updated successfully',
                        'phone': phone.serialize()}), 200

    except Exception as error:
        db.session.rollback()
        return jsonify({'error': 'Error updating phone'}), 500


@phone.route('/api/patch_phone/<int:id>', methods=['PATCH'])
def patch_phone(id):
    data = request.get_json()

    if not data:
        return jsonify({'error': 'No data received'}), 400

    phone = Phone.query.get(id)

    if not phone:
        return jsonify({'error': 'Phone not found'}), 404

    try:
        if 'phone' in data:
            phone.phone = data['phone']
        if 'id_client' in data:
            phone.id_client = data['id_client']

        db.session.commit()

        return jsonify({'message': 'Phone patched successfully',
                        'phone': phone.serialize()}), 200

    except Exception as error:
        db.session.rollback()
        return jsonify({'error': 'Error patching phone'}), 500


@phone.route('/api/sales_with_phones', methods=['GET'])
def get_sales_with_phones():
    from models.sale import Sale
    from models.phone import Phone

    try:
        sales = Sale.query.all()
        if not sales:
            return jsonify({'message': 'No sales found'}), 200

        result = []

        for sale in sales:
            phones = Phone.query.filter_by(id_client=sale.id_client).all()
            phone_list = [p.serialize() for p in phones]

            sale_data = sale.serialize()
            sale_data['phones'] = phone_list

            result.append(sale_data)

        return jsonify(result), 200

    except Exception as error:
        print(f'Error fetching sales with phones: {error}')
        return jsonify({'error': 'Error retrieving sales with phones'}), 500
