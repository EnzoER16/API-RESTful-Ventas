from models.db import db
from models.client import Client

class Sale(db.Model):
    __tablename__ = 'sales'

    id_sale = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    discount = db.Column(db.Float, nullable=False)
    amount = db.Column(db.Float, nullable=False)

    id_client = db.Column(db.Integer, db.ForeignKey('clients.id_client'), nullable=False)

    def __init__(self, date, discount, amount, id_client):
        self.date = date
        self.discount = discount
        self.amount = amount
        self.id_client = id_client

    def serialize(self):
        return {
            'id_sale': self.id_sale,
            'date': self.date,
            'id_client': self.id_client,
            'discount': self.discount,
            'amount': self.amount,
        }