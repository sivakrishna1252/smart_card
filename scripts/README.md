# Utility Scripts

These scripts are for database management and setup.

## How to Run

Since these scripts import from the `app` package, you should run them from the project root directory using the `-m` flag.

**Example:**

```bash
# Instead of running: python scripts/mowa_setup.py
# Run this from the root (smart_cart/):
python -m scripts.mowa_setup
```

## Available Scripts

- `mowa_setup.py`: Initial database setup.
- `simple_reset.py`: Resets the database (drops and recreates tables).
- `patch_mowa.py`: Applies patches to the database schema.
- `debug_db.py`: Debugging database connections.
