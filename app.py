import streamlit as st
from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import FAISS
from langchain.embeddings import OpenAIEmbeddings
from langchain.chat_models import ChatOpenAI
from langchain.chains import RetrievalQA
import os

st.set_page_config(page_title="Multilingual Chatbot")
st.title("🤖 Multilingual Chatbot (PDF + Normal Chat)")

if "OPENAI_API_KEY" not in os.environ:
    st.error("Please set OPENAI_API_KEY")
    st.stop()

llm = ChatOpenAI(temperature=0)

pdf = st.file_uploader("Upload PDF (optional)", type="pdf")
qa = None

if pdf:
    with open("temp.pdf", "wb") as f:
        f.write(pdf.read())

    loader = PyPDFLoader("temp.pdf")
    docs = loader.load()

    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    chunks = splitter.split_documents(docs)

    embeddings = OpenAIEmbeddings()
    vectorstore = FAISS.from_documents(chunks, embeddings)

    qa = RetrievalQA.from_chain_type(
        llm=llm,
        retriever=vectorstore.as_retriever()
    )

query = st.text_input("Ask your question:")

if query:
    if qa:
        st.write(qa.run(query))
    else:
        st.write(llm.predict(query))
