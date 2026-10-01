import streamlit as st
from rag import load_pdf

st.title("AI document Assistant")
uploaded_file = st.file_uploader(
    "upload a PDF",
    type=['pdf']
)

if uploaded_file:
    pages = load_pdf(uploaded_file)
    st.success(f"Loaded {len(pages)} pages.")
    st.write(pages[0]['text'][:2000])

