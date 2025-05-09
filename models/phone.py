from models.db import db
from models.client import Client

class Phone(db.Model):
    __tablename__ = 'phones'

    id_phone = db.Column(db.Integer, primary_key=True)
    phone = db.Column(db.String(20), nullable=False)

    id_client = db.Column(db.Integer, db.ForeignKey('clients.id_client'), nullable=False)

    def __init__(self, phone, id_client):
        self.phone = phone
        self.id_client = id_client

    def serialize(self):
        return {
            'id_phone': self.id_phone,
            'phone': self.phone,
            'id_client': self.id_client,
        }