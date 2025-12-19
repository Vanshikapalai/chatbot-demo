import streamlit as st
from transformers import pipeline
from langdetect import detect

st.set_page_config(page_title="Free AI Chatbot", page_icon="🤖")

st.title("🤖 Free AI Chatbot (No API Required)")
st.write("Supports multiple languages (basic)")

@st.cache_resource
def load_model():
    return pipeline(
        "text2text-generation",
        model="google/flan-t5-small"
    )

model = load_model()

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

user_input = st.chat_input("Type your message")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            prompt = f"Answer clearly: {user_input}"
            output = model(prompt, max_length=100)
            reply = output[0]["generated_text"]
            st.markdown(reply)

    st.session_state.messages.append({"role": "assistant", "content": reply})
