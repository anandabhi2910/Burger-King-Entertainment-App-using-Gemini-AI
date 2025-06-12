import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv() # Load environment variables from .env file

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    print("Error: GEMINI_API_KEY not found in your .env file.")
    exit()

genai.configure(api_key=GEMINI_API_KEY)

print("--- Available Gemini Models ---")
for m in genai.list_models():
    if 'generateContent' in m.supported_generation_methods:
        print(f"- {m.name}")
print("-----------------------------")