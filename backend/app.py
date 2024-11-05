from flask import Flask, request, jsonify
from flask_cors import CORS
import openai
from db import get_db_session, init_db, close_db_session
from models import User, Activity, Meal
import bcrypt
import jwt
import datetime
import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

app = Flask(__name__)
CORS(app)  # Esto habilita CORS para todas las rutas

# Configuración de claves secretas
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')

# Inicializar la base de datos
init_db()

# Configuración de OpenAI API
openai.api_key = os.getenv('OPENAI_API_KEY')

@app.before_request
def before_request():
    get_db_session()

@app.teardown_appcontext
def shutdown_session(exception=None):
    close_db_session()

@app.route('/ask', methods=['POST'])
def ask():
    data = request.get_json()
    question = data.get('question')

    # Lógica de ChatGPT
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=question,
        max_tokens=150
    )
    return jsonify({"answer": response.choices[0].text.strip()})

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    
    required_fields = ['username', 'password', 'fullName', 'weight', 'height', 'age', 'gender', 'goal', 'physicalActivityLevel', 'healthConditions']
    for field in required_fields:
        if field not in data:
            return jsonify({'message': f'{field} es requerido.'}), 400

    username = data['username']
    password = data['password']

    session = get_db_session()
    # Verificar si el usuario ya existe
    if session.query(User).filter_by(username=username).first():
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

    try:
        session.add(new_user)
        session.commit()
        return jsonify({'message': 'Usuario registrado exitosamente'}), 201
    except Exception as e:
        session.rollback()
        return jsonify({'error': str(e)}), 500

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({'message': 'Usuario y contraseña son requeridos'}), 400

    session = get_db_session()
    user = session.query(User).filter_by(username=username).first()

    if user and user.check_password(password):
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
        return jsonify({'message': 'Credenciales inválidas'}), 401

@app.route('/activities', methods=['POST'])
def add_activity():
    data = request.get_json()
    new_activity = Activity(
        user_id=data['user_id'],
        activity_type=data['activity_type'],
        description=data['description'],
        date=data['date'],
    )
    session = get_db_session()
    session.add(new_activity)
    session.commit()
    return jsonify({'message': 'Actividad registrada exitosamente'}), 201

@app.route('/meals', methods=['POST'])
def add_meal():
    data = request.get_json()
    new_meal = Meal(
        user_id=data['user_id'],
        meal_type=data['meal_type'],
        food_items=data['food_items'],
        calories=data['calories'],
        date=data['date'],
    )
    session = get_db_session()
    session.add(new_meal)
    session.commit()
    return jsonify({'message': 'Comida registrada exitosamente'}), 201

if __name__ == '__main__':
    app.run(debug=True, port=5000)