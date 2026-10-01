import streamlit as st
from rag import (
    load_pdf,
    chunk_pages,
    create_embeddings, 
    ask_question
)

st.title("AI document Assistant")
uploaded_file = st.file_uploader(
    "upload a PDF",
    type=['pdf']
)

if uploaded_file:
    pages = load_pdf(uploaded_file)
    chunks = chunk_pages(pages)

    embeddings = create_embeddings(chunks)

    st.write("Number of chunks:", len(chunks))
    st.write("Number of embeddings:", len(embeddings))

    st.write(
        "Embedding dimensions:",
        len(embeddings[0])
    )

    st.write(
        "First embedding:",
        embeddings[0][:10]
    )

question = st.text_input(
    "Ask a question about the document"
)

if question:
    answer, retrieved_chunks = ask_question(
        question,
        chunks,
        embeddings
    )

    st.subheader("Answer")
    st.write(answer)

    st.subheader("Retrieved Sources")

    for chunk in retrieved_chunks:
        st.write(
            f"Page {chunk['page']} | "
            f"Similarity: {chunk['score']:.3f}"
        )

        st.write(chunk["text"])
        st.divider()