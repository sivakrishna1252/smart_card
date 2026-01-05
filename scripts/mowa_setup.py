import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

def mowa_create_db():
    print("Mowa, creating smart_cart_v2 if it doesn't exist...", flush=True)
    try:
        # DB credentials from config
        user = "postgres"
        password = "xeda"
        host = "localhost"
        port = "5432"
        target_db = "smart_cart_v2"

        conn = psycopg2.connect(
            dbname="postgres",
            user=user,
            password=password,
            host=host,
            port=port
        )
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cursor = conn.cursor()

        cursor.execute(f"SELECT 1 FROM pg_database WHERE datname='{target_db}'")
        if not cursor.fetchone():
            print(f"Database {target_db} not found. Creating it mowa...", flush=True)
            cursor.execute(f"CREATE DATABASE {target_db}")
            print(f"Database {target_db} created successfully mowa!", flush=True)
        else:
            print(f"Database {target_db} already exists mowa.", flush=True)

        cursor.close()
        conn.close()

        # Now connect to the new DB and create tables
        print(f"Connecting to {target_db} to create tables mowa...", flush=True)
        from app.core.database import engine, Base
        from app.models.discount import Discount
        
        Base.metadata.create_all(bind=engine)
        print("✅ Tables created or already existed mowa!", flush=True)

    except Exception as e:
        print(f"❌ Mowa, something went wrong: {e}", flush=True)

if __name__ == "__main__":
    mowa_create_db()
