import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.ext.declarative import declarative_base

# Cargar variables de entorno
load_dotenv()
# Configuración de la base de datos
DATABASE_URL = f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"

# Crear el motor de SQLAlchemy con opciones de conexión
engine = create_engine(
    DATABASE_URL,
    echo=True,
    pool_size=5,
    max_overflow=10,
    pool_timeout=30,
    pool_recycle=1800
)

# Crear el motor de SQLAlchemy
engine = create_engine(DATABASE_URL, echo=True)

# Crear una fábrica de sesiones
session_factory = sessionmaker(bind=engine)

# Crear una sesión con ámbito
db_session = scoped_session(session_factory)

# Declarative Base para los modelos
Base = declarative_base()
Base.query = db_session.query_property()

def init_db():
    # Importar todos los módulos que contienen modelos aquí
    import models
    Base.metadata.create_all(bind=engine)

def get_db_session():
    return db_session

def close_db_session():
    db_session.remove()

if __name__ == "__main__":
    try:
        # Intenta crear una conexión
        connection = engine.connect()
        print("Conexión exitosa a la base de datos.")
        connection.close()
    except Exception as e:
        print(f"Error al conectar a la base de datos: {e}")
    finally:
        # Siempre cierra la sesión
        close_db_session()