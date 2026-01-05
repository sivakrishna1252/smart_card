from app.core.database import engine, Base
from app.models.discount import Discount
import sqlalchemy as sa

def reset():
    print("Dropping all tables...", flush=True)
    # Drop all existing tables to start fresh
    Base.metadata.drop_all(bind=engine)
    
    print("Creating only discounts table...", flush=True)
    # This will create tables defined in Base.metadata (only Discount now since others are unimported)
    from app.models.discount import Discount
    Base.metadata.create_all(bind=engine)
    print("Database reset successfully mowa!", flush=True)

if __name__ == "__main__":
    reset()
