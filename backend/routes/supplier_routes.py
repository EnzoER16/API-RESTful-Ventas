from flask import Blueprint, jsonify, request
from sqlalchemy.exc import IntegrityError
from models.db import db
from models.supplier import Supplier

supplier = Blueprint('supplier', __name__)

@supplier.route('/api/suppliers', methods=['GET'])
def get_suppliers():
    suppliers = Supplier.query.all()
    if not suppliers:
        return jsonify({'message': 'No suppliers found'}), 200
    return jsonify([supplier.serialize() for supplier in suppliers]), 200

@supplier.route('/api/add_supplier', methods=['POST'])
def add_supplier():
    data = request.get_json()

    if not data or not all(key in data for key in ['rut', 'name', 'address', 'phone', 'website']):
        return jsonify({'error': 'Missing required data'}), 400
    
    try:
        print(f'Data received: {data}')

        new_supplier = Supplier(
            data['rut'],
            data['name'],
            data['address'],
            data['phone'],
            data['website'])

        db.session.add(new_supplier)
        db.session.commit()

        return jsonify({'message': 'Supplier successfully added',
                        'supplier': new_supplier.serialize()}), 201

    except IntegrityError:
        db.session.rollback()

    except Exception as error:
        db.session.rollback()
        print(f'Unexpected error: {error}')
        return jsonify({'error': 'Error adding supplier'}), 500