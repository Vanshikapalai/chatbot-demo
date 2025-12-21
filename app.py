import streamlit as st
import google.generativeai as genai

# Configure API key
genai.configure(api_key="AIzaSyCKMH5q8lkjqb67odEY4Gz7WVYtlefHdjs")

# Create a model
model = genai.GenerativeModel("gemini-pro")

# Streamlit app
st.title("Chatbot Demo")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User input
if prompt := st.chat_input("What is up?"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate response
    response = model.generate_content(prompt)
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response.text})
    with st.chat_message("assistant"):
        st.markdown(response.text)
