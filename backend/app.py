from flask import Flask, request, jsonify, make_response
from flask_cors import CORS
import openai
import requests
import jwt
import datetime
import os
import logging
from functools import wraps
import bcrypt
from dotenv import load_dotenv
from db import get_db_session, close_db_session, init_db, User


# Configurar logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Cargar variables de entorno
load_dotenv()

app = Flask(__name__)
# Configura CORS de manera más permisiva
CORS(app, resources={
    r"/*": {
        "origins": [
            "http://localhost:8100",  # Ionic dev server
            "http://localhost:4200",  # Angular dev server
            "http://52.44.167.31:8100",  # Producción Ionic
            "http://52.44.167.31"  # Producción web
        ],
        "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization"]
    }
})

# Configuración de claves secretas
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')

# Configuración de OpenAI API
openai.api_key = os.getenv('OPENAI_API_KEY')

def get_db():
    db = get_db_session()
    try:
        yield db
    finally:
        close_db_session()

@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,POST,PUT,DELETE,OPTIONS')
    return response

@app.route('/login', methods=['POST'])
def login():
    if request.method == 'OPTIONS':
        response = make_response()
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
        response.headers.add('Access-Control-Allow-Methods', 'POST,OPTIONS')
        return response

    data = request.get_json()
    logging.debug(f'Datos recibidos en /login: {data}')

    # No se realiza verificación de credenciales
    return jsonify({
        'message': 'Inicio de sesión exitoso',
        'user': {
            'username': data.get('username', 'usuario_desconocido'),
            'full_name': data.get('fullName', 'Nombre Desconocido')
        }
    }), 200

@app.route('/register', methods=['POST'])
def register():
    if request.method == 'OPTIONS':
        response = make_response()
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
        response.headers.add('Access-Control-Allow-Methods', 'POST,OPTIONS')
        return response
    
    data = request.get_json()
    logging.debug(f'Datos recibidos en /register: {data}')
    
    required_fields = [
        'username', 'password', 'full_name', 'weight', 'height', 
        'age', 'gender', 'goal', 'physical_activityLevel', 'health_conditions'
    ]
    for field in required_fields:
        if field not in data or not data[field]:
            logging.error(f'Campo faltante o vacío: {field}')
            return jsonify({'message': f'{field} es requerido y no puede estar vacío'}), 400

    username = data['username']
    password = data['password']
    if len(password) < 8:
        return jsonify({'message': 'La contraseña debe tener al menos 8 caracteres'}), 400

    db = next(get_db())
    try:
        existing_user = db.query(User).filter_by(username=username).first()
        if existing_user:
            return jsonify({'message': 'El nombre de usuario ya existe'}), 400

        # Remove the line since "hashed_password" is not being used
        new_user = User(
        full_name=data['full_name'],
        username=data['username'],
        weight=data['weight'],
        height=data['height'],
        age=data['age'],
        gender=data['gender'],
        goal=data['goal'],
        physical_activity_level=int(data['physical_activity_level']),  # Asegurarse de que sea un entero
        health_conditions=data['health_conditions'] if data['health_conditions'] != 'none' else None
        )
        new_user.set_password(data['password'])
        db.add(new_user)
        db.commit()
        
        return jsonify({
            'message': 'Usuario registrado exitosamente', 
            'user': {
                'id': new_user.id,
                'username': new_user.username,
                'full_name': new_user.full_name
            }
        }), 201
    except ValueError as ve:
        db.rollback()
        logger.error(f"Error de conversión de datos: {str(ve)}")
        return jsonify({'error': 'Datos inválidos proporcionados'}), 400
    except Exception as e:
        db.rollback()
        logger.error(f"Error en registro: {str(e)}")
        return jsonify({'error': 'Error interno del servidor'}), 500
    finally:
        db.close()

from db import engine
from sqlalchemy import text

@app.route('/test-db', methods=['GET'])
def test_db():
    try:
        with engine.connect() as connection:
            result = connection.execute(text("SELECT * FROM users LIMIT 1;"))
            user = result.fetchone()
            if user:
                return jsonify({"message": "Conexión exitosa a la base de datos", "user": user}), 200
            return jsonify({"message": "Conexión exitosa, pero no se encontró ningún usuario"}), 200
    except Exception as e:
        logger.error(f"Error de conexión con la base de datos: {str(e)}")
        return jsonify({"message": "Error al conectar con la base de datos"}), 500

if __name__ == '__main__':
    app.run(debug=True)