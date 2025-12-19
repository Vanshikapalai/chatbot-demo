import streamlit as st
import os
from pypdf import PdfReader
import faiss
import numpy as np
from openai import OpenAI

st.set_page_config(page_title="🌍 Multilingual RAG Chatbot")
st.title("🌍 Multilingual RAG Chatbot")

# API key
if "OPENAI_API_KEY" not in os.environ:
    st.warning("Add OPENAI_API_KEY in Streamlit Secrets")

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

def get_embedding(text):
    res = client.embeddings.create(
        model="text-embedding-3-small",
        input=text
    )
    return np.array(res.data[0].embedding).astype("float32")

def chunk_text(text, size=800, overlap=100):
    chunks = []
    start = 0
    while start < len(text):
        chunks.append(text[start:start+size])
        start += size - overlap
    return chunks

pdf = st.file_uploader("Upload PDF", type="pdf")
query = st.text_input("Ask a question (any language)")

chunks = []
index = None

if pdf:
    reader = PdfReader(pdf)
    text = ""
    for page in reader.pages:
        text += page.extract_text() or ""

    chunks = chunk_text(text)
    embeddings = [get_embedding(c) for c in chunks]

    dim = len(embeddings[0])
    index = faiss.IndexFlatL2(dim)
    index.add(np.array(embeddings))

if query:
    if index:
        q_emb = get_embedding(query)
        _, I = index.search(np.array([q_emb]), k=3)
        context = "\n".join([chunks[i] for i in I[0]])
        prompt = f"Context:\n{context}\n\nQuestion:\n{query}"
    else:
        prompt = query

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )

    st.subheader("Answer")
    st.write(response.choices[0].message.content)
