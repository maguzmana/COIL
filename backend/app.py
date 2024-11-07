from flask import Flask, request, jsonify, make_response
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
from functools import wraps
import bcrypt

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
            "http://44.203.176.142:8100",  # Producción Ionic
            "http://44.203.176.142"  # Producción web
        ],
        "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization"]
    }
})

# Funciones de CORS
def add_cors_headers(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,POST,PUT,DELETE,OPTIONS')
    return response

@app.after_request
def after_request(response):
    return add_cors_headers(response)

# Manejador de preflight para todas las rutas
@app.route('/options', methods=['OPTIONS'])
def handle_options():
    response = make_response()
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,POST,PUT,DELETE,OPTIONS')
    return response

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

# Decorador de autenticación
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        
        # Verificar si el token está en los headers
        if 'Authorization' in request.headers:
            token = request.headers['Authorization'].split(" ")[1]
        
        if not token:
            return jsonify({'message': 'Token de autenticación no proporcionado'}), 401
        
        db = next(get_db())
        try:
            # Decodificar el token
            data = jwt.decode(token, JWT_SECRET_KEY, algorithms=['HS256'])
            current_user = db.query(User).filter_by(id=data['user_id']).first()
            
            if not current_user:
                return jsonify({'message': 'Usuario no encontrado'}), 401
        
        except jwt.ExpiredSignatureError:
            return jsonify({'message': 'Token expirado'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'message': 'Token inválido'}), 401
        except Exception as e:
            logger.error(f"Error en verificación de token: {str(e)}")
            return jsonify({'message': 'Error interno del servidor'}), 500
        finally:
            db.close()
        
        # Pasar el usuario actual a la función
        return f(current_user, *args, **kwargs)
    
    return decorated

# Rutas de autenticación y registro
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    logger.info(f"Intento de login para usuario: {username}")

    if not username or not password:
        return jsonify({'message': 'Usuario y contraseña son requeridos'}), 400

    db = next(get_db())
    try:
        user = db.query(User).filter_by(username=username).first()
        
        if not user:
            logger.warning(f"Usuario no encontrado: {username}")
            return jsonify({'message': 'Credenciales inválidas'}), 401

        # Verificar contraseña usando bcrypt
        if bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
            token = jwt.encode({
                'user_id': user.id,
                'username': user.username,
                'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=24)
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
    finally:
        db.close()

@app.route('/register', methods=['POST'])
def register():
    if request.method == 'OPTIONS':
        # Manejo de preflight
        response = make_response()
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
        response.headers.add('Access-Control-Allow-Methods', 'POST,OPTIONS')
        return response
    
    data = request.get_json()
    
    # Validación de campos requeridos
    required_fields = [
        'username', 'password', 'fullName', 'weight', 'height', 
        'age', 'gender', 'goal', 'physicalActivityLevel', 'healthConditions'
    ]
    for field in required_fields:
        if field not in data or not data[field]:
            return jsonify({'message': f'{field} es requerido y no puede estar vacío'}), 400

    username = data['username']
    password = data['password']

    # Validaciones adicionales
    if len(password) < 8:
        return jsonify({'message': 'La contraseña debe tener al menos 8 caracteres'}), 400

    db = next(get_db())
    try:
        # Verificar si el usuario ya existe
        existing_user = db.query(User).filter_by(username=username).first()
        if existing_user:
            return jsonify({'message': 'El nombre de usuario ya existe'}), 400

        # Generar hash de contraseña
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

        # Crear nuevo usuario
        new_user = User(
            username=username,
            full_name=data['fullName'],
            password=hashed_password.decode('utf-8'),  # Guardar como string
            weight=float(data['weight']),
            height=float(data['height']),
            age=int(data['age']),
            gender=data['gender'],
            goal=data['goal'],
            physical_activity_level=float(data['physicalActivityLevel']),
            # Convierte la lista de condiciones de salud a una cadena separada por comas
            health_conditions=','.join(data['healthConditions']) if data['healthConditions'] else None
        )

        # Añade y confirma el nuevo usuario
        db.add(new_user)
        db.commit()
        
        # Genera un token JWT
        token = jwt.encode({
            'user_id': new_user.id,
            'username': new_user.username,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=24)  # Token válido por 24 horas
        }, JWT_SECRET_KEY, algorithm='HS256')

        return jsonify({
            'message': 'Usuario registrado exitosamente', 
            'token': token,
            'user': {
                'id': new_user.id,
                'username': new_user.username,
                'full_name': new_user.full_name
            }
        }), 201

    except ValueError as ve:
        # Captura errores de conversión de tipos
        db.rollback()
        logger.error(f"Error de conversión de datos: {str(ve)}")
        return jsonify({'error': 'Datos inválidos proporcionados'}), 400

    except Exception as e:
        # Manejo genérico de errores
        db.rollback()
        logger.error(f"Error en registro: {str(e)}")
        return jsonify({'error': 'Error interno del servidor'}), 500

    finally:
        # Asegura que la sesión de base de datos se cierre
        db.close()

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

# Ejemplo de ruta protegida
@app.route('/perfil', methods=['GET'])
@token_required
def obtener_perfil(current_user):
    return jsonify({
        'id': current_user.id,
        'username': current_user.username,
        'full_name': current_user.full_name
    }), 200

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)