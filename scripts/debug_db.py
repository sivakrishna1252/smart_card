from sqlalchemy import create_engine, text
from app.core.config import settings

def check_db():
    print(f"Connecting to: {settings.DATABASE_URL}")
    try:
        engine = create_engine(settings.DATABASE_URL)
        with engine.connect() as connection:
            print("Connection successful!")
            result = connection.execute(text("SELECT * FROM discounts LIMIT 1;"))
            print("Discounts table check:", result.fetchall())
            
            result = connection.execute(text("SELECT * FROM orders LIMIT 1;"))
            print("Orders table check:", result.fetchall())
            
    except Exception as e:
        print(f"Database error: {e}")

if __name__ == "__main__":
    check_db()
