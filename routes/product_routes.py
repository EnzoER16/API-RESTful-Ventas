from flask import Blueprint, jsonify, request
from sqlalchemy.exc import IntegrityError
from models.db import db
from models.product import Product

product = Blueprint('product', __name__)

@product.route('/api/products', methods=['GET'])
def get_products():
    products = Product.query.all()
    if not products:
        return jsonify({'message': 'No products found'}), 200
    return jsonify([product.serialize() for product in products]), 200

@product.route('/api/add_product', methods=['POST'])
def add_product():
    data = request.get_json()

    if not data or not all(key in data for key in ['name', 'current_price', 'stock', 'id_supplier', 'id_category']):
        return jsonify({'error': 'Missing required data'}), 400
    
    try:
        print(f'Data received: {data}')

        new_product = Product(
            data['name'],
            data['current_price'],
            data['stock'],
            data['id_supplier'],
            data['id_category'])

        db.session.add(new_product)
        db.session.commit()

        return jsonify({'message': 'Product successfully added',
                        'product': new_product.serialize()}), 201

    except IntegrityError:
        db.session.rollback()
        return jsonify({'error': 'The product is already registered'}), 400

    except Exception as error:
        db.session.rollback()
        print(f'Unexpected error: {error}')
        return jsonify({'error': 'Error adding product'}), 500
    
@product.route('/api/delete_product/<int:id>', methods=['DELETE'])
def del_product(id):
    product = Product.query.get(id)

    if not product:
        return jsonify({'message': 'Product not found'}), 404
    
    try:
        db.session.delete(product)
        db.session.commit()
        return jsonify({'message': 'Product deleted successfully'}), 200
    
    except Exception as error:
        db.session.rollback()
        return jsonify({'error': 'Error deleting product'}), 500
    
@product.route('/api/update_product/<int:id>', methods=['PUT'])
def update_product(id):
    data = request.get_json()

    if not data:
        return jsonify({'error': 'No data received'}, 400)
    
    product = Product.query.get(id)

    if not product:
        return jsonify({'error': 'Product not found'}), 404
    
    try:
        product.name = data.get('name', product.name)
        product.current_price = data.get('current_price', product.current_price)
        product.stock = data.get('stock', product.stock)
        product.id_supplier = data.get('id_supplier', product.id_supplier)
        product.id_category = data.get('id_category', product.id_category)

        db.session.commit()

        return jsonify({'message': 'Product updated successfully',
                        'product': product.serialize()}), 200
    
    except Exception as error:
        db.session.rollback()
        return jsonify({'error': 'Error updating product'}), 500
    
@product.route('/api/patch_product/<int:id>', methods=['PATCH'])
def patch_product(id):
    data = request.get_json()

    if not data:
        return jsonify({'error': 'No data received'}), 400
    
    product = Product.query.get(id)

    if not product:
        return jsonify({'error': 'Product not found'}), 404
    
    try:
        if 'name' in data:
            product.name = data['name']
        if 'current_price' in data:
            product.current_price = data['current_price']
        if 'stock' in data:
            product.stock = data['stock']
        if 'id_supplier' in data:
            product.id_supplier = data['id_supplier']
        if 'id_category' in data:
            product.id_category = data['id_category']

        db.session.commit()

        return jsonify({'message': 'Product patched successfully',
                        'product': product.serialize()}), 200
    
    except Exception as error:
        db.session.rollback()
        return jsonify({'error': 'Error patching product'}), 500


@product.route('/api/products/top-selling', methods=['GET'])
def get_top_selling_products():
    try:
        top_products_query = db.session.query(
            SaleProduct.id_product,
            Product.name.label('product_name'),
            func.sum(SaleProduct.quantity).label('total_quantity_sold')
        ).join(
            Product, SaleProduct.id_product == Product.id_product
        ).group_by(
            SaleProduct.id_product, Product.name
        ).order_by(
            func.sum(SaleProduct.quantity).desc()
        ).limit(10).all()

        if not top_products_query:
            return jsonify({"message": "No sales data found to determine top selling products."}), 200

        top_products_list = []
        for product_data in top_products_query:
            top_products_list.append({
                "product_id": product_data.id_product,
                "product_name": product_data.product_name,
                "total_quantity_sold": int(product_data.total_quantity_sold) if product_data.total_quantity_sold is not None else 0
            })

        return jsonify(top_products_list), 200

    except Exception as e:
        print(f"Error fetching top selling products: {e}")
        return jsonify({"error": "An error occurred while fetching top selling products"}), 500
    
    
    @product.route('/api/products/top-selling', methods=['GET'])
def get_top_selling_products():
    try:
        top_products_query = db.session.query(
            SaleProduct.id_product,
            Product.name.label('product_name'),
            func.sum(SaleProduct.quantity).label('total_quantity_sold')
        ).join(
            Product, SaleProduct.id_product == Product.id_product
        ).group_by(
            SaleProduct.id_product, Product.name
        ).order_by(
            func.sum(SaleProduct.quantity).desc()
        ).limit(10).all()

        if not top_products_query:
            return jsonify({"message": "No sales data found to determine top selling products."}), 200

        top_products_list = []
        for product_data in top_products_query:
            top_products_list.append({
                "product_id": product_data.id_product,
                "product_name": product_data.product_name,
                "total_quantity_sold": int(product_data.total_quantity_sold) if product_data.total_quantity_sold is not None else 0
            })

        return jsonify(top_products_list), 200

    except Exception as e:
        print(f"Error fetching top selling products: {e}")
        return jsonify({"error": "An error occurred while fetching top selling products"}), 500