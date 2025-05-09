from models.db import db

class Client(db.Model):
    __tablename__ = 'clients'

    id_client = db.Column(db.Integer, primary_key=True)
    rut = db.Column(db.String(20), unique=True, nullable=False)
    name = db.Column(db.String(30), nullable=False)
    street = db.Column(db.String(50), nullable=False)
    number = db.Column(db.String(10))
    district = db.Column(db.String(30))
    city = db.Column(db.String(30))

    def __init__(self, rut, name, street, number, district, city):
        self.rut = rut
        self.name = name
        self.street = street
        self.number = number
        self.district = district
        self.city = city

    def serialize(self):
        return {
            'id_client': self.id_client,
            'rut': self.rut,
            'name': self.name,
            'street': self.street,
            'number': self.number,
            'district': self.district,
            'city': self.city
        }