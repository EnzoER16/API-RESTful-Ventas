from models.db import db

class Supplier(db.Model):
    __tablename__ = 'suppliers'

    id = db.Column(db.Integer, primary_key=True)
    rut = db.Column(db.String(20), nullable=False)
    name = db.Column(db.String(30), nullable=False)
    address = db.Column(db.String(50), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    website = db.Column(db.String(50), nullable=False)

    def __init__(self, rut, name, address, phone, website):
        self.rut = rut
        self.name = name
        self.address = address
        self.phone = phone
        self.website = website

    def serialize(self):
        return {
            'id': self.id,
            'rut': self.rut,
            'name': self.name,
            'address': self.address,
            'phone': self.phone,
            'website': self.website
        }