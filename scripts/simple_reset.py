import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from app.core.config import settings
from app.core.database import engine, Base
from app.models.discount import Discount

def reset():
    # 1. Parse URL
    db_url = settings.DATABASE_URL
    parts = db_url.replace("postgresql://", "").replace("@", ":").replace("/", ":").split(":")
    user = parts[0]
    password = parts[1]
    host = parts[2]
    port = parts[3]
    dbname = parts[4]

    print(f"Dropping all tables in {dbname} via psycopg2...", flush=True)
    try:
        conn = psycopg2.connect(
            dbname=dbname,
            user=user,
            password=password,
            host=host,
            port=port
        )
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cursor = conn.cursor()
        
        # Drop tables manually
        cursor.execute("DROP TABLE IF EXISTS orders_products CASCADE;")
        cursor.execute("DROP TABLE IF EXISTS orders CASCADE;")
        cursor.execute("DROP TABLE IF EXISTS products CASCADE;")
        cursor.execute("DROP TABLE IF EXISTS discounts CASCADE;")
        cursor.execute("DROP TABLE IF EXISTS alembic_version CASCADE;")
        
        cursor.close()
        conn.close()
        print("Tables dropped successfully.", flush=True)

        print("Creating tables via SQLAlchemy...", flush=True)
        Base.metadata.create_all(bind=engine)
        print("✅ Database reset successfully mowa!", flush=True)

    except Exception as e:
        print(f"❌ Reset failed: {e}", flush=True)

if __name__ == "__main__":
    reset()
