import psycopg2

def add_column():
    try:
        conn = psycopg2.connect(
            dbname="smart_crad",
            user="postgres",
            password="xeda",
            host="localhost",
            port="5432"
        )
        conn.autocommit = True
        cursor = conn.cursor()
        
        # Add column if not exists
        cursor.execute("""
            DO $$
            BEGIN
                IF NOT EXISTS (SELECT 1 FROM information_schema.columns 
                               WHERE table_name='orders' AND column_name='discount_percent') THEN
                    ALTER TABLE orders ADD COLUMN discount_percent DOUBLE PRECISION DEFAULT 0.0;
                END IF;
            END
            $$;
        """)
        print("✅ Column 'discount_percent' checked/added successfully!")
        cursor.close()
        conn.close()
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    add_column()
