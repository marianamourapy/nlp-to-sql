from sqlalchemy import text
from database.connection import get_connection


def run_query(sql: str) -> list:
    session = get_connection()
    try:
        result = session.execute(text(sql))
        return result.fetchall()
    finally:
        session.close()
