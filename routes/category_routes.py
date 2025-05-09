from flask import Blueprint, jsonify, request
from sqlalchemy.exc import IntegrityError
from models.db import db
from models.category import Category

category = Blueprint('category', __name__)

@category.route('/api/categories', methods=['GET'])
def get_categorys():
    categories = Category.query.all()
    if not categories:
        return jsonify({'message': 'No categories found'}), 200
    return jsonify([category.serialize() for category in categories]), 200

@category.route('/api/add_category', methods=['POST'])
def add_category():
    data = request.get_json()

    if not data or not all(key in data for key in ['name']):
        return jsonify({'error': 'Missing required data'}), 400
    
    try:
        print(f'Data received: {data}')

        new_category = Category(
            data['name'],
            data.get('description'))

        db.session.add(new_category)
        db.session.commit()

        return jsonify({'message': 'Category successfully added',
                        'category': new_category.serialize()}), 201

    except IntegrityError:
        db.session.rollback()
        return jsonify({'error': 'The category is already registered'}), 400

    except Exception as error:
        db.session.rollback()
        print(f'Unexpected error: {error}')
        return jsonify({'error': 'Error adding category'}), 500
    
@category.route('/api/delete_category/<int:id>', methods=['DELETE'])
def del_category(id):
    category = Category.query.get(id)

    if not category:
        return jsonify({'message': 'Category not found'}), 404
    
    try:
        db.session.delete(category)
        db.session.commit()
        return jsonify({'message': 'Category deleted successfully'}), 200
    
    except Exception as error:
        db.session.rollback()
        return jsonify({'error': 'Error deleting category'}), 500
    
@category.route('/api/update_category/<int:id>', methods=['PUT'])
def update_category(id):
    data = request.get_json()

    if not data:
        return jsonify({'error': 'No data received'}, 400)
    
    category = Category.query.get(id)

    if not category:
        return jsonify({'error': 'Category not found'}), 404
    
    try:
        category.name = data.get('name', category.name)
        category.description = data.get('description', category.description)

        db.session.commit()

        return jsonify({'message': 'Category updated successfully',
                        'category': category.serialize()}), 200
    
    except Exception as error:
        db.session.rollback()
        return jsonify({'error': 'Error updating category'}), 500
    
@category.route('/api/patch_category/<int:id>', methods=['PATCH'])
def patch_category(id):
    data = request.get_json()

    if not data:
        return jsonify({'error': 'No data received'}), 400
    
    category = Category.query.get(id)

    if not category:
        return jsonify({'error': 'Category not found'}), 404
    
    try:
        if 'name' in data:
            category.name = data['name']
        if 'description' in data:
            category.description = data['description']

        db.session.commit()

        return jsonify({'message': 'Category patched successfully',
                        'category': category.serialize()}), 200
    
    except Exception as error:
        db.session.rollback()
        return jsonify({'error': 'Error patching category'}), 500