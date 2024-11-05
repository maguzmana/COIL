from flask import Flask, request, jsonify
from flask_cors import CORS
import openai
from db import get_db_session, init_db, close_db_session
from models import User, Activity, Meal
import bcrypt
import jwt
import datetime

app = Flask(__name__)
CORS(app)  # Esto habilita CORS para todas las rutas

# Inicializar la base de datos
init_db()

# Configuración de OpenAI API
openai.api_key = "sk-your-api-key"  # Cambia esto por tu clave real

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

    # Encriptar la contraseña
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

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
        health_conditions=data['healthConditions'],
        password_hash=hashed_password
    )

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

    if user and bcrypt.checkpw(password.encode('utf-8'), user.password_hash.encode('utf-8')):
        token = jwt.encode({
            'user_id': user.id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)
        }, "your_secret_key", algorithm='HS256')

        return jsonify({'token': token}), 200
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