import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from pathlib import Path
from core.logger import get_logger

load_dotenv()

logger = get_logger(__name__)

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    pool_recycle=300,
    pool_size=5,
    max_overflow=2
    )

SessionLocal = sessionmaker(bind=engine)

BASE_DIR = Path(__file__).parent
SCHEMA_PATH = BASE_DIR / "schema.sql"


def get_connection():
   return SessionLocal()


def initialize_database():
    try:
        with open(SCHEMA_PATH, "r") as f:
            schema = f.read()

        with engine.connect() as conn:
            conn.execute(text(schema))
            conn.commit()

        logger.info("Database initialized successfully!")

    except Exception as e:
        logger.error(f"Failed to initialize database: {str(e)}")
        raise


if __name__ == "__main__":
    initialize_database()
