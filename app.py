import streamlit as st
import google.generativeai as genai

# Configure API key
genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
# or: genai.configure(api_key="YOUR_API_KEY")

st.title("AI Language Agnostic Chatbot")

# ✅ Use a supported model
model = genai.GenerativeModel("gemini-1.5-flash")

prompt = st.text_input("Type your message")

if prompt:
    response = model.generate_content(prompt)
    st.write(response.text)
