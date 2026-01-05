import psycopg2

try:
    conn = psycopg2.connect(
        dbname="smart_crad",
        user="postgres",
        password="xeda",
        host="localhost",
        port="5432"
    )
    print("✅ Connection successful!")
    conn.close()
except Exception as e:
    print(f"❌ Connection failed: {e}")
