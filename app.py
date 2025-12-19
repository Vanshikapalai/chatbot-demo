import streamlit as st

st.set_page_config(page_title="Language Agnostic Chatbot")

st.title("🤖 Language Agnostic Chatbot")
st.write("Ask anything in any language")

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

user_input = st.chat_input("Type your message here...")

if user_input:
    st.session_state.messages.append(
        {"role": "user", "content": user_input}
    )

    with st.chat_message("user"):
        st.markdown(user_input)

    # Simple chatbot logic (safe & guaranteed)
    response = f"You said: {user_input}"

    st.session_state.messages.append(
        {"role": "assistant", "content": response}
    )

    with st.chat_message("assistant"):
        st.markdown(response)
