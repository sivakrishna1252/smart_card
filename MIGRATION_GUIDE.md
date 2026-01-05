# PostgreSQL Migration Guide

## Setup Steps

### 1. Install PostgreSQL Driver
```bash
pip install psycopg2-binary
```

### 2. Create Database in PostgreSQL
```sql
CREATE DATABASE smart_card;
```

Or using command line:
```bash
psql -U postgres
CREATE DATABASE smart_card;
\q
```

### 3. Run Migrations

#### Create Initial Migration
```bash
cd smart_cart
alembic revision --autogenerate -m "Initial migration"
```

#### Apply Migration
```bash
alembic upgrade head
```

### 4. Check Migration Status
```bash
alembic current
alembic history
```

## Migration Commands

| Command | Description |
|---------|-------------|
| `alembic revision --autogenerate -m "message"` | Create new migration |
| `alembic upgrade head` | Apply all migrations |
| `alembic downgrade -1` | Rollback last migration |
| `alembic current` | Show current migration |
| `alembic history` | Show all migrations |

## Database Configuration

Current settings (in `app/core/config.py`):
```
Host: localhost
Port: 5432
Database: smart_card
Username: postgres
Password: siva
```

## Troubleshooting

### If database doesn't exist:
```bash
psql -U postgres
CREATE DATABASE smart_card;
\q
```

### If connection fails:
1. Check PostgreSQL is running
2. Verify password is correct
3. Check database exists
4. Verify port 5432 is open
