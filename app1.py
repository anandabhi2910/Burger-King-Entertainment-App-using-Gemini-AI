import streamlit as st
import pandas as pd

# --- Configuration for Data File ---
# Set this to 'orders.xlsx' if you created an Excel file,
# or 'orders.csv' if you created a CSV file.
DATA_FILE_NAME = 'orders.csv'

# Set this to 'excel' if you created an Excel file,
# or 'csv' if you created a CSV file.
DATA_FILE_TYPE = 'csv'

# --- Function to load data ---
# @st.cache_data decorator caches the data loading, so it only runs once
# unless the file changes, making the app faster.
# Set basic page configuration
st.set_page_config(
    page_title="Burger King Engage & Entertain",
    page_icon="🍔", # A nice burger icon for the browser tab
    layout="centered" # Centers the content on the page
)
@st.cache_data
def load_order_data(file_name, file_type):
    """Loads order data from the specified Excel or CSV file."""
    try:
        if file_type == 'excel':
            df = pd.read_excel(file_name)
        elif file_type == 'csv':
            df = pd.read_csv(file_name)
        else:
            st.error(f"Error: Unsupported data file type '{file_type}'. Please use 'excel' or 'csv'.")
            return pd.DataFrame() # Return an empty DataFrame on error
        
        # Ensure 'OrderID' column is treated as string to avoid issues with numbers
        # (e.g., if an ID were '007', pandas might read it as 7)
        df['OrderID'] = df['OrderID'].astype(str)
        return df
    except FileNotFoundError:
        st.error(f"Error: Data file '{file_name}' not found. Make sure it's in the same directory as 'app.py'.")
        return pd.DataFrame()
    except Exception as e:
        st.error(f"An error occurred while loading the data: {e}")
        return pd.DataFrame()

# Load the order data when the app starts
orders_df = load_order_data(DATA_FILE_NAME, DATA_FILE_TYPE)

# --- Streamlit Application UI ---

# Set basic page configuration
# st.set_page_config(
#     page_title="Burger King Engage & Entertain",
#     page_icon="🍔", # A nice burger icon for the browser tab
#     layout="centered" # Centers the content on the page
# )

# Application Title
st.title("🍔 Burger King - Engage & Entertain 🎮")
st.markdown("---") # A horizontal line for separation

# Introduction text
st.header("Your Order Experience")
st.write("Scan the QR code on your menu and enter your Order ID below to start the fun!")

# Input field for the Order ID
# max_chars: Limits the length of the input
# placeholder: Provides example text when the field is empty
order_id_input = st.text_input(
    "Enter your Order ID:",
    max_chars=10,
    placeholder="e.g., 38",
    help="Type the order ID found on your receipt or given by the cashier."
)

# --- Logic to Display Order Details ---
# This block runs only if the user has entered something in the order_id_input
if order_id_input:
    # Check if the orders_df is empty (e.g., if file loading failed)
    if orders_df.empty:
        st.warning("Cannot retrieve order details because the data could not be loaded.")
    else:
        # Filter the DataFrame to find the matching order ID
        # .loc is used for label-based indexing
        # We compare the input string to the 'OrderID' column (which we made sure is string type)
        found_order = orders_df.loc[orders_df['OrderID'] == order_id_input]

        # Check if an order was actually found (i.e., the filtered DataFrame is not empty)
        if not found_order.empty:
            st.subheader(f"Details for Order ID: `{order_id_input}`") # Use backticks for monospace font

            # Extract the 'Items' and 'Status' from the first (and only) matching row
            items = found_order['Items'].iloc[0]
            status = found_order['Status'].iloc[0]

            st.success("Order Found! 🎉") # Green success message
            st.write(f"**Items:** {items}")
            st.write(f"**Status:** {status}")

            st.markdown("---") # Another separator

            # --- Options Menu (Placeholder for Future Features) ---
            st.subheader("What would you like to do while you wait?")
            
            # Use columns to arrange buttons horizontally
            col1, col2, col3 = st.columns(3) 

            with col1:
                # Button for Fun Facts
                if st.button("💡 Fun Facts about your order"):
                    st.info("Great choice! Fun facts will appear here soon. Stay tuned! 😉")
                    # Future: Call a function to fetch and display relevant fun facts
                    # Example: display_fun_facts(items)

            with col2:
                # Button for Quizzes
                if st.button("🧠 Play a Quiz"):
                    st.info("Get ready to test your knowledge! Quizzes are on their way. 🤓")
                    # Future: Call a function to start a quiz related to order items
                    # Example: start_order_quiz(items)

            with col3:
                # Button for Games
                if st.button("🎮 Play a Short Game"):
                    st.info("Time to play! Mini-games are being prepared. 🚀")
                    # Future: Call a function to display or launch a mini-game
                    # Example: launch_mini_game()

        else:
            # Message if the order ID is not found
            st.warning(f"Order ID `{order_id_input}` not found. Please double-check and try again.")
            st.info("Currently, our system only recognizes Order IDs: 38, 39, 40, and 41.")

# Footer
st.markdown("---")
st.caption("Developed by abhishek for Burger King customers. Enjoy your wait! 😊")