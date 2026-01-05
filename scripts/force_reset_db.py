import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from app.core.config import settings

def force_reset():
    db_url = settings.DATABASE_URL
    # Parse URL manually for psycopg2
    # postgresql://postgres:xeda@localhost:5432/smart_crad
    parts = db_url.replace("postgresql://", "").replace("@", ":").replace("/", ":").split(":")
    user = parts[0]
    password = parts[1]
    host = parts[2]
    port = parts[3]
    dbname = parts[4]

    print(f"Connecting to 'postgres' to clear '{dbname}'...", flush=True)
    try:
        conn = psycopg2.connect(
            dbname="postgres",
            user=user,
            password=password,
            host=host,
            port=port
        )
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cursor = conn.cursor()

        # Terminate other sessions
        print(f"Terminating other sessions for '{dbname}'...", flush=True)
        cursor.execute(f"""
            SELECT pg_terminate_backend(pg_stat_activity.pid)
            FROM pg_stat_activity
            WHERE pg_stat_activity.datname = '{dbname}'
              AND pid <> pg_backend_pid();
        """)
        
        # Drop and recreate database or just tables? 
        # Recreating tables is enough if columns changed.
        cursor.close()
        conn.close()

        print("Sessions cleared. Now dropping and creating tables...", flush=True)
        from app.core.database import engine, Base
        from app.models.discount import Discount
        
        # We need to make sure Base is associated with the Discount model
        Base.metadata.drop_all(bind=engine)
        print("Tables dropped.", flush=True)
        Base.metadata.create_all(bind=engine)
        print("Tables created with new schema.", flush=True)
        print("✅ Database force reset successfully mowa!", flush=True)

    except Exception as e:
        print(f"❌ Force reset failed: {e}", flush=True)

if __name__ == "__main__":
    force_reset()
