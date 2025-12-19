import streamlit as st
import os

from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_openai import ChatOpenAI
from langchain.chains import RetrievalQA

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="🌍 Multilingual RAG Chatbot")

st.title("🌍 Multilingual RAG Chatbot")

# ---------------- API KEY CHECK ----------------
if "OPENAI_API_KEY" not in os.environ:
    st.warning("⚠️ Please add your OpenAI API key in Streamlit Secrets")

# ---------------- PDF UPLOAD ----------------
pdf = st.file_uploader("📄 Upload a PDF", type="pdf")

# ---------------- NORMAL CHAT INPUT ----------------
query = st.text_input("💬 Ask your question (any language):")

# ---------------- LOGIC ----------------
if pdf:
    with open("temp.pdf", "wb") as f:
        f.write(pdf.read())

    loader = PyPDFLoader("temp.pdf")
    documents = loader.load()

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=100
    )
    chunks = splitter.split_documents(documents)

    embeddings = OpenAIEmbeddings()
    vectorstore = FAISS.from_documents(chunks, embeddings)

    llm = ChatOpenAI(temperature=0)

    qa = RetrievalQA.from_chain_type(
        llm=llm,
        retriever=vectorstore.as_retriever()
    )

    if query:
        answer = qa.run(query)
        st.subheader("✅ Answer")
        st.write(answer)

else:
    if query:
        llm = ChatOpenAI(temperature=0)
        answer = llm.predict(query)
        st.subheader("✅ Answer")
        st.write(answer)
