from flask import Flask
from config.config import SQLALCHEMY_DATABASE_URI, SQLALCHEMY_TRACK_MODIFICATIONS
from models.db import db
from routes.client_routes import client
from routes.products_routes import product
from routes.vehicle_routes import vehicle
from routes.service_routes import service
from routes.payment_routes import payment

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = SQLALCHEMY_TRACK_MODIFICATIONS

app.register_blueprint(client)
app.register_blueprint(product)
app.register_blueprint(vehicle)
app.register_blueprint(service)
app.register_blueprint(payment)

db.init_app(app)

with app.app_context():
    from models.client import Client
    from models.products import Products
    from models.vehicle import Vehicle
    from models.service import Service
    from models.payment import Payment
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)