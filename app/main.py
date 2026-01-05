from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.core.database import engine, Base
from app.api import discounts_router, cart_router

from sqlalchemy import text

# patch logic mowa
def patch_database():
    with engine.connect() as connection:
        with connection.begin():
            # Drop old column if it exists to avoid constraint violations mowa
            try:
                connection.execute(text("ALTER TABLE discounts DROP COLUMN IF EXISTS minimum_threshold"))
            except Exception as e:
                print(f"Drop old col failed: {e}")

            # Add new columns if missing
            cols = {
                "min_unique_products": "INTEGER DEFAULT 3",
                "target_amount": "FLOAT DEFAULT 10000",
                "max_discount_cap": "FLOAT DEFAULT 800"
            }
            for col, dtype in cols.items():
                try:
                    connection.execute(text(f"ALTER TABLE discounts ADD COLUMN IF NOT EXISTS {col} {dtype}"))
                except Exception as e:
                    print(f"Patch skip {col}: {e}")

# Apply patch and create tables
try:
    patch_database()
except Exception as e:
    print(f"Patch failed: {e}")

Base.metadata.create_all(bind=engine)

app = FastAPI(title=settings.PROJECT_NAME)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include Routers
app.include_router(discounts_router)
app.include_router(cart_router)

@app.get("/")
def read_root():
    return {"message": "Welcome to Smart Cart API"}

from fastapi import Request
from fastapi.responses import JSONResponse
import traceback

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    error_msg = str(exc)
    stack_trace = traceback.format_exc()
    print(f"Global Exception: {error_msg}\n{stack_trace}")
    return JSONResponse(
        status_code=500,
        content={
            "message": "Internal Server Error", 
            "detail": error_msg,
            "trace": stack_trace.splitlines()[-3:] # Send last 3 lines of trace for safety/brevity
        },
    )
