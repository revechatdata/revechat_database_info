import pandas as pd
from sqlalchemy import create_engine, text
from urllib.parse import quote_plus
from sqlalchemy.exc import SQLAlchemyError
import os

# --- MySQL Connection Parameters (GitHub Secrets) ---
mysql_user = os.getenv("MYSQL_USER")
mysql_password = quote_plus(os.getenv("MYSQL_PASSWORD"))
mysql_host = os.getenv("MYSQL_HOST")
mysql_db = os.getenv("MYSQL_DB")

# --- PostgreSQL (DWH) Connection Parameters (GitHub Secrets) ---
pg_user = os.getenv("PG_USER")
pg_password = os.getenv("PG_PASSWORD")
pg_host = os.getenv("PG_HOST")
pg_port = os.getenv("PG_PORT", "5432")
pg_db = os.getenv("PG_DB")

# --- Create MySQL Engine ---
mysql_engine = create_engine(
    f"mysql+pymysql://{mysql_user}:{mysql_password}@{mysql_host}/{mysql_db}",
    pool_pre_ping=True
)

# --- Create PostgreSQL Engine ---
pg_engine = create_engine(
    f"postgresql+psycopg2://{pg_user}:{pg_password}@{pg_host}:{pg_port}/{pg_db}",
    pool_pre_ping=True
)

# ============================
# INCREMENTAL ETL CONFIG
# ============================
SOURCE_TABLE = "vbmissedchats"
TARGET_TABLE = "vbmissedchats"

CHUNK_SIZE = 10000
INSERT_CHUNK = 5000

try:
    print(f"\n===== Starting Incremental ETL for table: {SOURCE_TABLE} =====")

    # STEP 1: Get last loaded ID from DWH
    with pg_engine.connect() as conn:
        result = conn.execute(text(f"SELECT COALESCE(MAX(id), 0) FROM {TARGET_TABLE}"))
        last_id = result.scalar()

    print(f"🔎 Last loaded ID in DWH: {last_id}")

    # STEP 2: Read only new data from MySQL
    query = f"""
        SELECT *
        FROM {SOURCE_TABLE}
        WHERE id > {last_id}
        ORDER BY id
    """

    rows_loaded = 0

    for chunk in pd.read_sql(query, mysql_engine, chunksize=CHUNK_SIZE):
        chunk.columns = [c.lower() for c in chunk.columns]

        chunk.to_sql(
            TARGET_TABLE,
            pg_engine,
            if_exists="append",
            index=False,
            chunksize=INSERT_CHUNK,
            method="multi"
        )

        rows_loaded += len(chunk)
        print(f"📥 Inserted {len(chunk)} new rows")

    if rows_loaded == 0:
        print("ℹ️ No new records found")

    print(f"✅ Incremental ETL completed — Total new rows: {rows_loaded}")

finally:
    mysql_engine.dispose()
    pg_engine.dispose()
    print("🔒 All connections closed")
