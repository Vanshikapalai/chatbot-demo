import streamlit as st
from transformers import pipeline

st.set_page_config(page_title="Language Agnostic Chatbot")
st.title("🌍 Language Agnostic Chatbot")
st.write("Ask anything in any language")

@st.cache_resource
def load_model():
    return pipeline(
        "text2text-generation",
        model="google/flan-t5-small"
    )

model = load_model()

user_input = st.text_input("Type your message")

if user_input:
    with st.spinner("Thinking..."):
        result = model(user_input, max_length=100)
        st.write(result[0]["generated_text"])
