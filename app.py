import streamlit as st

st.set_page_config(page_title="Language Agnostic Chatbot")

st.title("😄 Language Agnostic Chatbot")
st.write("Ask anything in any language")

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

user_input = st.chat_input("Type your message here...")

def bot_reply(text):
    text = text.lower()
    if "hello" in text or "hi" in text:
        return "Hello! 😊 How can I help you?"
    elif "how are you" in text:
        return "I'm doing great! Thanks for asking 😄"
    elif "name" in text:
        return "I'm a Language Agnostic Chatbot 🤖"
    else:
        return "I understood your message, but I'm a demo chatbot."

if user_input:
    st.session_state.messages.append(
        {"role": "user", "content": user_input}
    )

    with st.chat_message("user"):
        st.markdown(user_input)

    response = bot_reply(user_input)

    st.session_state.messages.append(
        {"role": "assistant", "content": response}
    )

    with st.chat_message("assistant"):
        st.markdown(response)
