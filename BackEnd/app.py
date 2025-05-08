from flask import Flask
from config.config import DATABASE_CONNECTION_URI
from models.db import db

def create_app():
    app = Flask(__name__)

    # Configuración de la base de datos
    app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_CONNECTION_URI
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Inicializar la DB
    db.init_app(app)

    @app.route('/')
    def index():
        return "API Flask funcionando ✅"

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
