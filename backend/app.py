""" app.py """

from flask import Flask, request, jsonify
from flask_cors import CORS
import openai
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, User, Activity, Meal
import jwt
import datetime
import os
from dotenv import load_dotenv
import logging

# Configurar logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Cargar variables de entorno
load_dotenv()

app = Flask(__name__)
CORS(app)

# Configuración de la base de datos
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')
DB_NAME = os.getenv('DB_NAME')

DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# Crear el engine de SQLAlchemy
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Crear las tablas
Base.metadata.create_all(bind=engine)

# Configuración de claves secretas
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')

# Configuración de OpenAI API
openai.api_key = os.getenv('OPENAI_API_KEY')

def get_db():
    db = SessionLocal()
    try:
        return db
    finally:
        db.close()

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    logger.info(f"Intento de login para usuario: {username}")

    if not username or not password:
        return jsonify({'message': 'Usuario y contraseña son requeridos'}), 400

    db = get_db()
    try:
        user = db.query(User).filter_by(username=username).first()
        
        if not user:
            logger.warning(f"Usuario no encontrado: {username}")
            return jsonify({'message': 'Credenciales inválidas'}), 401

        logger.info(f"Usuario encontrado: {username}")
        
        if user.check_password(password):
            logger.info("Contraseña correcta")
            token = jwt.encode({
                'user_id': user.id,
                'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)
            }, JWT_SECRET_KEY, algorithm='HS256')

            return jsonify({
                'token': token,
                'user': {
                    'id': user.id,
                    'username': user.username,
                    'full_name': user.full_name
                }
            }), 200
        else:
            logger.warning("Contraseña incorrecta")
            return jsonify({'message': 'Credenciales inválidas'}), 401

    except Exception as e:
        logger.error(f"Error en login: {str(e)}")
        return jsonify({'message': 'Error en el servidor'}), 500

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    
    required_fields = ['username', 'password', 'fullName', 'weight', 'height', 'age', 'gender', 'goal', 'physicalActivityLevel', 'healthConditions']
    for field in required_fields:
        if field not in data:
            return jsonify({'message': f'{field} es requerido.'}), 400

    username = data['username']
    password = data['password']

    db = get_db()
    try:
        # Verificar si el usuario ya existe
        if db.query(User).filter_by(username=username).first():
            return jsonify({'message': 'El nombre de usuario ya existe'}), 400

        # Crear nuevo usuario
        new_user = User(
            username=data['username'],
            full_name=data['fullName'],
            weight=float(data['weight']),
            height=float(data['height']),
            age=int(data['age']),
            gender=data['gender'],
            goal=data['goal'],
            physical_activity_level=float(data['physicalActivityLevel']),
            health_conditions=data['healthConditions']
        )
        new_user.set_password(password)

        db.add(new_user)
        db.commit()
        return jsonify({'message': 'Usuario registrado exitosamente'}), 201
    except Exception as e:
        db.rollback()
        logger.error(f"Error en registro: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/test-connection', methods=['GET'])
def test_connection():
    logger.info("Probando conexión a la base de datos...")
    try:
        db = get_db()
        users_count = db.query(User).count()
        logger.info(f"Conexión exitosa. Número de usuarios: {users_count}")
        return jsonify({
            'status': 'success',
            'message': 'Conexión exitosa',
            'users_count': users_count
        }), 200
    except Exception as e:
        logger.error(f"Error en la conexión: {str(e)}")
        return jsonify({
            'status': 'error',
            'message': f'Error de conexión: {str(e)}'
        }), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)