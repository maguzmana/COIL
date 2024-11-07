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
from sqlalchemy import text
from dotenv import load_dotenv
import logging
from werkzeug.security import generate_password_hash, check_password_hash

# Configurar logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Cargar variables de entorno
load_dotenv()

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": ["http://localhost:4200", "http://localhost:8100", "http://35.174.155.239:8100", "http://35.174.155.239"]}})

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
        yield db
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

    # Comentar o eliminar la verificación de credenciales
    """
    db = next(get_db())
    try:
        user = db.query(User).filter_by(username=username).first()
        
        if not user:
            logger.warning(f"Usuario no encontrado: {username}")
            return jsonify({'message': 'Credenciales inválidas'}), 401

        logger.info(f"Usuario encontrado: {username}")
        
        logger.debug(f"Campos del usuario: {', '.join(user.__dict__.keys())}")

        if user.check_password(password):
            logger.info("Contraseña correcta")
            # ... (resto del código)
        else:
            logger.warning("Contraseña incorrecta")
            return jsonify({'message': 'Credenciales inválidas'}), 401

    except Exception as e:
        logger.error(f"Error en login: {str(e)}")
        return jsonify({'message': 'Error en el servidor'}), 500
    """

    # Aceptar cualquier credencial
    logger.info("Modo de desarrollo: Aceptando cualquier credencial")
    token = jwt.encode({
        'user_id': 1,  # ID de usuario ficticio
        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)
    }, JWT_SECRET_KEY, algorithm='HS256')

    return jsonify({
        'token': token,
        'user': {
            'id': 1,
            'username': username,
            'full_name': 'Usuario de Desarrollo'
        }
    }), 200
    
@app.route('/test-db', methods=['GET'])
def test_db():
    try:
        with engine.connect() as connection:
            result = connection.execute(text("SELECT * FROM users LIMIT 1"))
            rows = [dict(row) for row in result]
            
            if rows:
                # Asegúrate de no incluir la contraseña en los logs
                safe_row = {k: v for k, v in rows[0].items() if k != 'password' and k != 'password_hash'}
                logger.info(f"Primer usuario en la base de datos: {safe_row}")
                return jsonify({"message": "Consulta exitosa", "data": safe_row}), 200
            else:
                return jsonify({"message": "No se encontraron usuarios"}), 404
    except Exception as e:
        logger.error(f"Error al consultar la base de datos: {str(e)}")
        return jsonify({"message": "Error al consultar la base de datos"}), 500

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    
    required_fields = ['username', 'password', 'fullName', 'weight', 'height', 'age', 'gender', 'goal', 'physicalActivityLevel', 'healthConditions']
    for field in required_fields:
        if field not in data:
            return jsonify({'message': f'{field} es requerido.'}), 400

    username = data['username']
    password = data['password']

    db = next(get_db())
    try:
        # Verificar si el usuario ya existe
        if db.query(User).filter_by(username=username).first():
            return jsonify({'message': 'El nombre de usuario ya existe'}), 400

        # Crear nuevo usuario
        hashed_password = generate_password_hash(password)
        new_user = User(
            username=data['username'],
            password=hashed_password,
            full_name=data['fullName'],
            weight=float(data['weight']),
            height=float(data['height']),
            age=int(data['age']),
            gender=data['gender'],
            goal=data['goal'],
            physical_activity_level=float(data['physicalActivityLevel']),
            health_conditions=data['healthConditions']
        )

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
        db = next(get_db())
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
