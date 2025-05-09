from models.db import db
from models.sale import Sale

class SaleProduct(db.Model):
    __tablename__ = 'sale_products'

    id_sale_product = db.Column(db.Integer, primary_key=True)
    price_at_sale = db.Column(db.Float, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    subtotal = db.Column(db.Float, nullable=False)

    id_sale = db.Column(db.Integer, db.ForeignKey('sales.id_sale'), nullable=False)
    id_product = db.Column(db.Integer, db.ForeignKey('products.id_product'), nullable=False)

    def __init__(self, price_at_sale, quantity, subtotal, id_sale, id_product):
        self.price_at_sale = price_at_sale
        self.quantity = quantity
        self.subtotal = subtotal
        self.id_sale = id_sale
        self.id_product = id_product

    def serialize(self):
        return {
            'id_sale_product': self.id_sale_product,
            'price_at_sale': self.price_at_sale,
            'quantity': self.quantity,
            'subtotal': self.subtotal,
            'id_sale': self.id_sale,
            'id_product': self.id_product
        }