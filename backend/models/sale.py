from models.db import db
from models.client import Client

class Sale(db.Model):
    __tablename__ = 'sales'

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    client_id = db.Column(db.Integer, db.ForeignKey('clients.id'))
    discount = db.Column(db.Float)
    amount = db.Column(db.Float)

    def __init__(self, date, client_id, discount, amount):
        self.date = date
        self.client_id = client_id
        self.discount = discount
        self.amount = amount

    def serialize(self):
        return {
            'id': self.id,
            'date': self.date,
            'client_id': self.client_id,
            'discount': self.discount,
            'amount': self.amount,
        }