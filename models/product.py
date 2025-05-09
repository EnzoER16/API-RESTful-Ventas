from models.db import db
from models.supplier import Supplier
from models.category import Category

class Product(db.Model):
    __tablename__ = 'products'
    
    id_product = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    current_price = db.Column(db.Float, nullable=False)
    stock = db.Column(db.Integer, nullable=False)

    id_supplier = db.Column(db.Integer, db.ForeignKey('suppliers.id_supplier'), nullable=False)
    id_category = db.Column(db.Integer, db.ForeignKey('categories.id_category'), nullable=False)

    def __init__(self, name, current_price, stock, id_supplier, id_category):
        self.name = name
        self.current_price = current_price
        self.stock = stock
        self.id_supplier = id_supplier
        self.id_category = id_category

    def serialize(self):
        return {
            'id_product': self.id_product,
            'name': self.name,
            'name': self.current_price,
            'stock': self.stock,
            'id_supplier': self.id_supplier,
            'id_category': self.id_category,
        }