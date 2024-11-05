from db import engine

def test_connection():
    try:
        with engine.connect() as connection:
            print("Conexión exitosa!")
            result = connection.execute("SELECT version();")
            print(result.fetchone())
    except Exception as e:
        print(f"Error de conexión: {e}")

if __name__ == "__main__":
    test_connection()