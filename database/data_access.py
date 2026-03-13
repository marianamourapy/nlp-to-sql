from database.executor import run_query


def get_all_customers():
    return run_query("SELECT * FROM customers")

def get_all_products():
    return run_query("SELECT * FROM products")

def get_sales_overview():
    return run_query(""" 
        SELECT
            customers.name AS customer,
            products.name AS product,
            sales.quantity,
            sales.date
        FROM sales
        JOIN customers ON sales.customer_id = customers.id
        JOIN products ON sales.product_id = products.id
""")