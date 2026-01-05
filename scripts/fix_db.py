import psycopg2
from app.core.config import settings

def fix_database():
    print(f"Connecting to database: {settings.DATABASE_URL}")
    try:
        # Connect to the database
        conn = psycopg2.connect(settings.DATABASE_URL)
        conn.autocommit = True
        cur = conn.cursor()
        
        # Done (Column removed from code, no need to add to DB)
        print("Refusing to add min_unique_products as it has been removed from codebase.")
            
        cur.close()
        conn.close()
        print("Done.")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    fix_database()
