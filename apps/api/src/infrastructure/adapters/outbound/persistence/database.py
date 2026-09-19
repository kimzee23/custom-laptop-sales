import ssl
from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import declarative_base
from src.infrastructure.config.settings import settings

Base = declarative_base()

connect_args = {}
db_url = settings.async_database_url

if db_url.startswith("sqlite"):
    connect_args = {"check_same_thread": False}
elif "postgresql" in db_url:
    # If connecting to remote PostgreSQL (e.g. Render, Supabase, Neon)
    if "localhost" not in db_url and "127.0.0.1" not in db_url:
        ssl_ctx = ssl.create_default_context()
        ssl_ctx.check_hostname = False
        ssl_ctx.verify_mode = ssl.CERT_NONE
        connect_args = {"ssl": ssl_ctx}

async_engine = create_async_engine(
    db_url,
    echo=False,
    future=True,
    connect_args=connect_args
)

AsyncSessionLocal = async_sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False
)

async def get_db_session():
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()

async def run_auto_migrations():
    """
    Safely ensures any newly added columns exist in existing tables.
    Runs idempotently for both SQLite and PostgreSQL.
    """
    async with async_engine.begin() as conn:
        # Check dialect
        is_postgres = "postgresql" in settings.async_database_url
        
        column_patches = [
            ("users", "is_verified", "BOOLEAN DEFAULT FALSE NOT NULL" if is_postgres else "BOOLEAN DEFAULT 0 NOT NULL"),
            ("users", "otp_code", "VARCHAR(10)"),
            ("users", "otp_expires_at", "TIMESTAMP" if is_postgres else "DATETIME"),
            ("categories", "updated_at", "TIMESTAMP" if is_postgres else "DATETIME"),
            ("brands", "created_at", "TIMESTAMP" if is_postgres else "DATETIME"),
            ("brands", "updated_at", "TIMESTAMP" if is_postgres else "DATETIME"),
            ("configuration_categories", "created_at", "TIMESTAMP" if is_postgres else "DATETIME"),
            ("configuration_categories", "updated_at", "TIMESTAMP" if is_postgres else "DATETIME"),
            ("configuration_options", "created_at", "TIMESTAMP" if is_postgres else "DATETIME"),
            ("configuration_options", "updated_at", "TIMESTAMP" if is_postgres else "DATETIME"),
            ("cart_items", "created_at", "TIMESTAMP" if is_postgres else "DATETIME"),
            ("cart_items", "updated_at", "TIMESTAMP" if is_postgres else "DATETIME"),
            ("order_items", "created_at", "TIMESTAMP" if is_postgres else "DATETIME"),
            ("order_items", "updated_at", "TIMESTAMP" if is_postgres else "DATETIME"),
            ("processed_webhook_events", "created_at", "TIMESTAMP" if is_postgres else "DATETIME"),
            ("processed_webhook_events", "updated_at", "TIMESTAMP" if is_postgres else "DATETIME"),
            ("reviews", "updated_at", "TIMESTAMP" if is_postgres else "DATETIME"),
            ("addresses", "updated_at", "TIMESTAMP" if is_postgres else "DATETIME"),
            ("saved_configurations", "updated_at", "TIMESTAMP" if is_postgres else "DATETIME"),
            ("promotions", "updated_at", "TIMESTAMP" if is_postgres else "DATETIME"),
            ("visitor_logs", "updated_at", "TIMESTAMP" if is_postgres else "DATETIME"),
        ]

        for table, column, col_type in column_patches:
            try:
                if is_postgres:
                    await conn.execute(text(f"ALTER TABLE {table} ADD COLUMN IF NOT EXISTS {column} {col_type};"))
                else:
                    # SQLite doesn't support IF NOT EXISTS in ADD COLUMN; ignore duplicate column error
                    await conn.execute(text(f"ALTER TABLE {table} ADD COLUMN {column} {col_type};"))
            except Exception:
                # Column already exists or table not yet created
                pass
