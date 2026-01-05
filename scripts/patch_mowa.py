import psycopg2
from app.core.config import settings

def patch_db():
    print("Mowa, patching smart_crad to add missing columns...", flush=True)
    try:
        db_url = settings.DATABASE_URL
        # Parse URL
        parts = db_url.replace("postgresql://", "").replace("@", ":").replace("/", ":").split(":")
        user = parts[0]
        password = parts[1]
        host = parts[2]
        port = parts[3]
        dbname = parts[4]

        conn = psycopg2.connect(
            dbname=dbname,
            user=user,
            password=password,
            host=host,
            port=port
        )
        conn.autocommit = True
        cursor = conn.cursor()

        # Add columns if they don't exist
        columns_to_add = {
            "min_unique_products": "INTEGER DEFAULT 3",
            "target_amount": "FLOAT DEFAULT 10000",
            "max_discount_cap": "FLOAT DEFAULT 800"
        }

        for col, dtype in columns_to_add.items():
            try:
                cursor.execute(f"ALTER TABLE discounts ADD COLUMN {col} {dtype}")
                print(f"Added column {col} mowa!", flush=True)
            except psycopg2.Error as e:
                if "already exists" in str(e):
                    print(f"Column {col} already exists mowa.", flush=True)
                else:
                    raise e

        # Also drop unused columns if any (optional but good for cleanup)
        try:
            cursor.execute("ALTER TABLE discounts DROP COLUMN IF EXISTS minimum_threshold")
            print("Dropped old column minimum_threshold mowa!", flush=True)
        except:
            pass

        cursor.close()
        conn.close()
        print("✅ Patching completed successfully mowa!", flush=True)

    except Exception as e:
        print(f"❌ Mowa, patching failed: {e}", flush=True)

if __name__ == "__main__":
    patch_db()
