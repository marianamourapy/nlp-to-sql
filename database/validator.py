import sqlparse
from core.logger import get_logger

logger = get_logger(__name__)

def validate_sql(sql: str) -> tuple[bool, str]:
    if not sql or not sql.strip():
        logger.warning("Empty query received.")
        return False, "Empty query."
    
    parsed = sqlparse.parse(sql)

    if not parsed:
        logger.warning("Could not parse query.")
        return False, "Could not parse the query."
    
    statement = parsed[0]
    query_type = statement.get_type()

    if query_type != "SELECT":
        logger.warning(f"Invalid query type: {query_type} | SQL: {sql}")
        return False, f"Only SELECT queries are allowed. Got {query_type}"
    
    logger.debug(f"Valid query: {sql}")
    return True, "Valid query."