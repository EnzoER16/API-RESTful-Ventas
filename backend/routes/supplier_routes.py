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
    
@supplier.route('/api/delete_supplier', methods=['DELETE'])
def del_supplier():
    supplier = Supplier.query.get(id)

    if not supplier:
        return jsonify({'message': 'Supplier not found'}), 404
    
    try:
        db.session.delete(supplier)
        db.session.commit()
        return jsonify({'message': 'Supplier deleted successfully'}), 200
    
    except Exception as error:
        db.session.rollback()
        return jsonify({'error': 'Error deleting supplier'}), 500
    
@supplier.route('/api/update_supplier', methods=['PUT'])
def update_supplier():
    data = request.get_json()

    if not data:
        return jsonify({'error': 'No data received'}, 400)
    
    supplier = Supplier.query.get(id)

    if not supplier:
        return jsonify({'error': 'Supplier not found'}), 404
    
    try:
        supplier.rut = data.get('rut', supplier.rut)
        supplier.name = data.get('name', supplier.name)
        supplier.address = data.get('address', supplier.address)
        supplier.phone = data.get('phone', supplier.phone)
        supplier.website = data.get('website', supplier.website)

        db.session.commit()

        return jsonify({'message': 'Supplier updated successfully',
                        'supplier': supplier.serialize()}), 200
    
    except Exception as error:
        db.session.rollback()
        return jsonify({'error': 'Error updating supplier'}), 500
    
@supplier.route('/api/patch_supplier', methods=['PATCH'])
def patch_supplier():
    data = request.get_json()

    if not data:
        return jsonify({'error': 'No data received'}), 400
    
    supplier = Supplier.query.get(id)

    if not supplier:
        return jsonify({'error': 'Supplier not found'}), 404
    
    try:
        if 'rut' in data:
            supplier.rut = data['rut']
        if 'name' in data:
            supplier.name = data['name']
        if 'address' in data:
            supplier.address = data['address']
        if 'phone' in data:
            supplier.phone = data['phone']
        if 'website' in data:
            supplier.website = data['website']

        db.session.commit()

        return jsonify({'message': 'Supplier patched successfully',
                        'supplier': supplier.serialize()}), 200
    
    except Exception as error:
        db.session.rollback()
        return jsonify({'error': 'Error patching supplier'}), 500