from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

class Proveedor(db.Model):
    __tablename__ = 'proveedor'

    rut = db.Column(db.String(15), primary_key=True)
    name = db.Column(db.String(25), nullable=False)
    address = db.Column(db.String(50), nullable=False)
    phone = db.Column(db.String(15), unique=True, nullable=False)
    website = db.Column(db.String(50), unique=True)

    def __init__(self, name, address, phone, website):
        self.name = name
        self.address = address
        self.phone = phone
        self.website = website

    def serialize(self):
        return {
            'rut': self.rut,
            'name': self.name,
            'address': self.address,
            'phone': self.phone,
            'website': self.website
        }