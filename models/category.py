from models.db import db

class Category(db.Model):
    __tablename__ = 'categories'

    id_category = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    description = db.Column(db.String(50))

    def __init__(self, name, description):
        self.name = name
        self.description = description

    def serialize(self):
        return {
            'id': self.id_category,
            'name': self.name,
            'description': self.description,
        }