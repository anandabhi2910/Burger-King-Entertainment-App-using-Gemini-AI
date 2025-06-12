import sqlite3

DB_NAME = 'burger_king_new.db'

def create_tables():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    # Enable foreign key constraints
    cursor.execute("PRAGMA foreign_keys = ON;")

    # 1. Create Customers Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS customers (
            customer_id INTEGER PRIMARY KEY AUTOINCREMENT,
            mobile_number TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE, -- Email can be optional (NULL)
            points INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    ''')

    # 2. Create Orders Table (if it doesn't exist, or alter it if it does)
    # This approach handles if 'orders' table already exists,
    # it adds the customer_id column without recreating the table.
    # Note: If 'orders' table already has data, customer_id will be NULL for existing rows.
    # We'll link sample orders to customers in add_sample_data.
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS orders (
            order_id INTEGER PRIMARY KEY,
            items TEXT NOT NULL,
            status TEXT NOT NULL,
            customer_id INTEGER, -- New column for linking to customers
            FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
        );
    ''')

    # Add customer_id column to existing orders table if it doesn't exist
    try:
        cursor.execute("ALTER TABLE orders ADD COLUMN customer_id INTEGER;")
        cursor.execute("ALTER TABLE orders ADD FOREIGN KEY (customer_id) REFERENCES customers(customer_id);")
    except sqlite3.OperationalError as e:
        if "duplicate column name" in str(e):
            print("customer_id column already exists in orders table. Skipping ALTER TABLE.")
        else:
            print(f"Error altering orders table: {e}")


    conn.commit()
    conn.close()

def add_sample_data():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    # Clear existing data before adding new samples to avoid duplicates
    cursor.execute("DELETE FROM orders;")
    cursor.execute("DELETE FROM customers;")

    # Add sample customers
    customers_data = [
        ('9876543210', 'john.doe@example.com'),
        ('9988776655', 'jane.smith@example.com'),
        ('9123456789', None), # Customer without email
    ]
    cursor.executemany("INSERT INTO customers (mobile_number, email) VALUES (?, ?)", customers_data)
    
    # Get customer IDs for linking
    cursor.execute("SELECT customer_id, mobile_number FROM customers;")
    customer_ids = {row[1]: row[0] for row in cursor.fetchall()} # Map mobile_number to customer_id

    # Add sample orders linked to customers
    # Ensure order_id is managed (e.g., start from a certain number or use AUTOINCREMENT if not already set)
    # For simplicity, we'll manually assign order_ids here.
    orders_data = [
        (38, 'Whopper Meal, Fries, Coke', 'Ready for Pickup', customer_ids.get('9876543210')),
        (39, 'Chicken Nuggets (9 pcs), Diet Coke', 'In Progress', customer_ids.get('9988776655')),
        (40, 'Veggie Burger, Onion Rings', 'Ready for Pickup', customer_ids.get('9876543210')), # John's second order
        (41, 'Coffee, Muffin', 'New Order', customer_ids.get('9123456789')), # New customer's order
        (42, 'Crispy Chicken Sandwich', 'New Order', None), # Anonymous order
    ]
    cursor.executemany("INSERT INTO orders (order_id, items, status, customer_id) VALUES (?, ?, ?, ?)", orders_data)

    conn.commit()
    conn.close()

if __name__ == '__main__':
    create_tables()
    add_sample_data()
    print("Database tables created and sample data added/updated with customer tracking.")