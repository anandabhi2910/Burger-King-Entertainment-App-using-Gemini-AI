import streamlit as st
import sqlite3
import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# --- Configuration for Database ---
DB_NAME = 'burger_king.db'

# --- Configuration for Gemini API ---
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    st.error("Gemini API Key not found. Please set GEMINI_API_KEY in your .env file.")
    st.stop() # Stop the app if API key is missing

# Configure the generative AI model
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash-latest') # Using 'gemini-pro' for text generation

# --- Database Functions (from previous step) ---
@st.cache_resource
def get_db_connection():
    conn = sqlite3.connect(DB_NAME, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn

def get_order_details(order_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT OrderID, Items, Status FROM orders WHERE OrderID = ?", (order_id,))
    order_data = cursor.fetchone()
    return order_data

# --- AI Integration: Fun Fact Generation Function ---
@st.cache_data(ttl=3600) # Cache facts for 1 hour to reduce API calls
def generate_fun_fact(item_name):
    """
    Generates a fun fact about a given item using the Gemini API.
    Includes a fallback for API errors or empty responses.
    """
    if not item_name:
        return "Did you know: Enjoying your meal is the most fun fact!"

    # Fallback facts in case API fails or for generic items
    fallback_facts = {
        "burger": [
            "Did you know: The hamburger's origin is debated, but many believe it came from Hamburg, Germany!",
            "Fun fact: The world's largest hamburger weighed over 2,000 pounds!"
        ],
        "coke": [
            "Did you know: Coca-Cola was originally invented as a patent medicine!",
            "Fun fact: Coca-Cola is the most widely distributed product in the world, available in over 200 countries."
        ],
        "whopper": [
            "Did you know: The Whopper was introduced by Burger King in 1957!",
            "Fun fact: The Whopper got its name because Burger King wanted to convey a sense of a large, satisfying burger."
        ],
        "fries": [
            "Did you know: French fries might actually originate from Belgium, not France!",
            "Fun fact: Thomas Jefferson is often credited with introducing 'French Fried Potatoes' to America."
        ]
    }

    # Clean item name for better prompting
    clean_item = item_name.replace("x", "").strip().split(' ')[-1].lower() # e.g., "2x Burger" -> "burger"

    # Try to get a specific fallback if available
    if clean_item in fallback_facts and fallback_facts[clean_item]:
        # Return a random fallback if we're also using it for API failure
        import random
        selected_fallback = random.choice(fallback_facts[clean_item])
    else:
        selected_fallback = "Did you know: Food tastes better when you're having fun!"


    try:
        # Construct the prompt
        prompt = f"Give me one very short, engaging, and fun fact about {clean_item} relevant to fast food. Make it sound like a quick trivia tidbit. Do not include intros like 'Here's a fun fact' or 'Did you know', just the fact itself."

        # Generate content with Gemini API
        response = model.generate_content(prompt)

        # Check for valid response and content
        if response and response.candidates and response.candidates[0].content and response.candidates[0].content.parts:
            fact = response.candidates[0].content.parts[0].text
            # Basic moderation check (optional, but good practice)
            if "i cannot fulfill this request" in fact.lower() or "not appropriate" in fact.lower():
                return selected_fallback # Use fallback if AI refuses
            return fact
        else:
            st.warning("AI did not return a valid fact. Using a fallback fact.")
            return selected_fallback

    except Exception as e:
        st.error(f"Error generating AI fact: {e}. Using a fallback fact.")
        return selected_fallback

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
    order_details = get_order_details(order_id_input)

    if order_details:
        st.subheader(f"Details for Order ID: `{order_id_input}`")
        items = order_details['Items']
        status = order_details['Status']

        st.success("Order Found! 🎉")
        st.write(f"**Items:** {items}")
        st.write(f"**Status:** {status}")

        st.markdown("---")

        # --- Options Menu ---
        st.subheader("What would you like to do while you wait?")

        col1, col2, col3 = st.columns(3)

        with col1:
            if st.button("💡 Fun Facts about your order"):
                with st.spinner("Generating fun fact..."): # Show a spinner while AI works
                    # Extract main item from the order (e.g., "Burger" from "2x Burger, 1x Coke")
                    # This is a simple parsing, could be more robust
                    first_item = items.split(',')[0].strip() # Takes "2x Burger"
                    
                    fun_fact = generate_fun_fact(first_item)
                    st.info(fun_fact) # Display the generated fact

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