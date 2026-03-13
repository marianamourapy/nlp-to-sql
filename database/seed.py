from sqlalchemy import text
from database.connection import get_connection
from core.logger import get_logger

logger = get_logger(__name__)

def seed_database():
    session = get_connection()
    try:
        session.execute(text("""
            INSERT INTO customers (name, email, city) VALUES
            ('Alice Johnson', 'alice_johnson@gmail.com', 'New York'),
            ('Bob Smith', 'bob_smith@gmail.com', 'Florida'),
            ('Walter White', 'walter_white@gmail.com', 'Albuquerque'),
            ('Carol White', 'carol_white@gmail.com', 'Albuquerque'),
            ('David Brown', 'david_brown@gmail.com', 'San Francisco')
            ON CONFLICT (email) DO NOTHING
        """))

        session.execute(text("""
            INSERT INTO products (name, price, stock) VALUES
            ('Macbook', 999.99, 5),
            ('Samsung TV', 255.99, 10),
            ('Headphones', 24.99, 7)
            ON CONFLICT (name) DO NOTHING
        """))

        session.execute(text("""
            INSERT INTO sales (customer_id, product_id, quantity, date) VALUES
            (1, 1, 1, '2024-01-15'),
            (2, 2, 2, '2024-01-20'),
            (3, 3, 1, '2024-02-05'),
            (4, 2, 1, '2024-02-10'),
            (5, 3, 1, '2024-02-14'),
            (1, 2, 3, '2024-03-01'),
            (2, 1, 2, '2024-03-15'),
            (3, 1, 1, '2024-03-20')
        """))

        session.commit()
        logger.info("Database seeded successfully!")

    except Exception as e:
        session.rollback()
        logger.error(f"Error seeding database: {e}")
    finally:
        session.close()


if __name__ == "__main__":
    seed_database()