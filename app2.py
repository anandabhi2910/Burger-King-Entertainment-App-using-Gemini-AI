import streamlit as st
import sqlite3

# --- Configuration for Database ---
DB_NAME = 'burger_king.db'

# --- Function to connect to the database and fetch data ---
@st.cache_resource # Use st.cache_resource for database connections
def get_db_connection():
    """Establishes and returns a database connection."""
    conn = sqlite3.connect(DB_NAME, check_same_thread=False)
    conn.row_factory = sqlite3.Row # This allows access to columns by name
    return conn

def get_order_details(order_id):
    """Fetches order details for a given OrderID from the database."""
    conn = get_db_connection()
    cursor = conn.cursor()
    # Use parameterized query to prevent SQL injection
    cursor.execute("SELECT OrderID, Items, Status FROM orders WHERE OrderID = ?", (order_id,))
    order_data = cursor.fetchone() # Fetch a single row

    # No need to close connection here, it's managed by st.cache_resource
    # and connection is reused.

    return order_data # Returns a sqlite3.Row object or None if not found

# --- Streamlit Application UI ---

st.set_page_config(
    page_title="Burger King Engage & Entertain",
    page_icon="🍔",
    layout="centered"
)

st.title("🍔 Burger King - Engage & Entertain 🎮")
st.markdown("---")

st.header("Your Order Experience")
st.write("Scan the QR code on your menu and enter your Order ID below to start the fun!")

# Input field for the Order ID
order_id_input = st.text_input(
    "Enter your Order ID:",
    max_chars=10,
    placeholder="e.g., 38",
    help="Type the order ID found on your receipt or given by the cashier."
)

# --- Logic to Display Order Details ---
if order_id_input:
    # Attempt to fetch order details from the database
    order_details = get_order_details(order_id_input)

    if order_details: # If order_details is not None
        st.subheader(f"Details for Order ID: `{order_id_input}`")

        # Access data using column names from the sqlite3.Row object
        items = order_details['Items']
        status = order_details['Status']

        st.success("Order Found! 🎉")
        st.write(f"**Items:** {items}")
        st.write(f"**Status:** {status}")

        st.markdown("---")

        # --- Options Menu (Placeholder for Future Features) ---
        st.subheader("What would you like to do while you wait?")

        col1, col2, col3 = st.columns(3)

        with col1:
            if st.button("💡 Fun Facts about your order"):
                st.info("Great choice! Fun facts will appear here soon. Stay tuned! 😉")

        with col2:
            if st.button("🧠 Play a Quiz"):
                st.info("Get ready to test your knowledge! Quizzes are on their way. 🤓")

        with col3:
            if st.button("🎮 Play a Short Game"):
                st.info("Time to play! Mini-games are being prepared. 🚀")

    else:
        st.warning(f"Order ID `{order_id_input}` not found. Please double-check and try again.")
        st.info("Currently, our system recognizes Order IDs: 38, 39, 40, and 41.")

st.markdown("---")
st.caption("Developed by abhishek for Burger King customers. Enjoy your wait! 😊")