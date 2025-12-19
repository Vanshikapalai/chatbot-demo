import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="AI Language Agnostic Chatbot")
st.title("🤖 AI Language Agnostic Chatbot (Gemini)")
st.write("Ask anything in any language")

# Load API key
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

model = genai.GenerativeModel("gemini-pro")

if "chat" not in st.session_state:
    st.session_state.chat = model.start_chat(history=[])

user_input = st.text_input("Type your message")

if user_input:
    with st.spinner("Thinking..."):
        response = st.session_state.chat.send_message(user_input)
        st.success(response.text)
