import os
from dotenv import load_dotenv

load_dotenv()


def str_to_bool(value: str) -> bool:
    return value.lower() in ("true", "1", "yes")


GROQ_API_KEY = os.getenv("GROQ_API_KEY")

ENVIRONMENT_TYPE = os.getenv("ENVIRONMENT", "development")

DEBUG_MODE = str_to_bool(os.getenv("DEBUG", "False"))

if ENVIRONMENT_TYPE == "production":
    DEBUG_MODE = False

CLASSIFIER_MODEL = "llama-3.3-70b-versatile"
SQL_MODEL = "llama-3.3-70b-versatile"
INTERPRETER_MODEL = "llama-3.3-70b-versatile"
CONTEXT_RESOLVER_MODEL = "llama-3.3-70b-versatile"

SCHEMA_CONTEXT = """
You have access to a PostgreSQL database with the following tables:

customers (id, name, email, city)
products (id, name, price, stock)
sales (id, customer_id, product_id, quantity, date)

Relationships:
- sales.customer_id references customers.id
- sales.product_id references products.id
"""
