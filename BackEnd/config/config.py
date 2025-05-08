from dotenv import load_dotenv
import os

# Cargar variables del archivo .env
load_dotenv()

# Leer la URI desde el entorno
DATABASE_CONNECTION_URI = os.getenv('DATABASE_URI')
