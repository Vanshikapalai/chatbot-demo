import streamlit as st
import requests

st.set_page_config(page_title="AI Language Agnostic Chatbot")
st.title("🤖 AI Language Agnostic Chatbot (Gemini)")
st.write("Ask anything in any language")

API_KEY = st.secrets["GEMINI_API_KEY"]

def ask_gemini(prompt):
    url = (
        "https://generativelanguage.googleapis.com/v1beta/models/"
        "gemini-pro:generateContent?key=" + API_KEY
    )

    headers = {"Content-Type": "application/json"}
    data = {
        "contents": [
            {
                "parts": [{"text": prompt}]
            }
        ]
    }

    response = requests.post(url, headers=headers, json=data)
    result = response.json()

    # 🔒 SAFE PARSING
    if "candidates" in result:
        return result["candidates"][0]["content"]["parts"][0]["text"]
    else:
        return f"❌ Gemini Error:\n{result}"

user_input = st.text_input("Type your message")

if user_input:
    with st.spinner("Thinking..."):
        answer = ask_gemini(user_input)
        st.success(answer)
