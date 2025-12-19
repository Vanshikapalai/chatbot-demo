import streamlit as st
import os
from pypdf import PdfReader
import faiss
import numpy as np
from openai import OpenAI

# ---------------- CONFIG ----------------
st.set_page_config(page_title="🌍 Multilingual RAG Chatbot")
st.title("🌍 Multilingual RAG Chatbot")

# ---------------- API KEY ----------------
if "OPENAI_API_KEY" not in os.environ:
    st.warning("⚠️ Please add your OpenAI API key in Streamlit Secrets")

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

# ---------------- HELPERS ----------------
def get_embedding(text):
    response = client.embeddings.create(
        model="text-embedding-3-small",
        input=text
    )
    return np.array(response.data[0].embedding, dtype="float32")

def chunk_text(text, size=800, overlap=100):
    chunks = []
    start = 0
    while start < len(text):
        chunks.append(text[start:start+size])
        start += size - overlap
    return chunks

# ---------------- PDF UPLOAD ----------------
pdf = st.file_uploader("📄 Upload a PDF", type="pdf")
query = st.text_input("💬 Ask your question (any language):")

texts = []
index = None

if pdf:
    reader = PdfReader(pdf)
    full_text = ""
    for page in reader.pages:
        full_text += page.extract_text() or ""

    chunks = chunk_text(full_text)

    embeddings = [get_embedding(c) for c in chunks]
    dim = len(embeddings[0])

    index = faiss.IndexFlatL2(dim)
    index.add(np.array(embeddings))

# ---------------- CHAT ----------------
if query:
    if index:
        q_emb = get_embedding(query)
        D, I = index.search(np.array([q_emb]), k=3)
        context = "\n".join([chunks[i] for i in I[0]])

        prompt = f"""Answer the question using the context below.
If context is insufficient, say so.

Context:
{context}

Question:
{query}
"""
    else:
        prompt = query

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )

    st.subheader("✅ Answer")
    st.write(response.choices[0].message.content)
