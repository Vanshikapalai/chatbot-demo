import streamlit as st
from openai import OpenAI

# Page config
st.set_page_config(page_title="Language Agnostic AI Chatbot", page_icon="🤖")

st.title("🤖 Language Agnostic AI Chatbot")
st.write("Ask anything in **any language**")

# Initialize OpenAI client
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# Chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# User input
user_input = st.chat_input("Type your message here...")

if user_input:
    # Show user message
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # AI response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are a helpful multilingual assistant."},
                    *st.session_state.messages
                ]
            )
            ai_reply = response.choices[0].message.content
            st.markdown(ai_reply)

    st.session_state.messages.append({"role": "assistant", "content": ai_reply})

