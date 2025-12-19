import streamlit as st
import openai
import os

st.set_page_config(page_title="Chatbot Demo")
st.title("💬 AI Chatbot")

# API Key
if "OPENAI_API_KEY" not in os.environ:
    st.warning("Please set OPENAI_API_KEY in Streamlit secrets")
    st.stop()

openai.api_key = os.environ["OPENAI_API_KEY"]

user_input = st.text_input("Ask anything:")

if user_input:
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": user_input}
        ]
    )
    st.write("### Answer")
    st.write(response.choices[0].message.content)
