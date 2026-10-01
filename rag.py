
import re
import os
from pypdf import PdfReader
import numpy as np
from sentence_transformers import SentenceTransformer
from dotenv import load_dotenv
from openai import OpenAI

def load_pdf(file):
    reader = PdfReader(file)
    pages = []
    for page_number, page in enumerate(reader.pages):
        text = page.extract_text()
        if text:
            pages.append({
                "text": text,
                "page": page_number + 1
            })

    return pages


def split_into_sentences(text):
    sentences = re.split(
        r"(?<=[.!?])\s+",
        text
    )

    return [
        sentence.strip()
        for sentence in sentences
        if sentence.strip()
    ]


def split_list(input_list, slice_size):
    return [
        input_list[i:i + slice_size]
        for i in range(0, len(input_list), slice_size)
    ]


def chunk_pages(pages, sentences_per_chunk=10):
    chunks = []

    for page in pages:
        sentences = split_into_sentences(page["text"])

        sentence_groups = split_list(
            sentences,
            sentences_per_chunk
        )

        for group in sentence_groups:
            chunk_text = " ".join(group)

            chunks.append({
                "text": chunk_text,
                "page": page["page"],
                "sentence_count": len(group)
            })

    return chunks



embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

def create_embeddings(chunks):
    texts = [
        chunk["text"]
        for chunk in chunks
    ]

    embeddings = embedding_model.encode(
        texts
    )

    return embeddings

def retrieve_top_k(question, chunks, embeddings, top_k=3):
    question_embedding = embedding_model.encode([question])[0]

    # Normalize vectors
    chunk_vectors = embeddings / np.linalg.norm(
        embeddings,
        axis=1,
        keepdims=True
    )

    question_vector = question_embedding / np.linalg.norm(
        question_embedding
    )

    # Cosine similarity
    similarities = chunk_vectors @ question_vector

    top_indices = np.argsort(similarities)[::-1][:top_k]

    results = []

    for index in top_indices:
        results.append({
            "text": chunks[index]["text"],
            "page": chunks[index]["page"],
            "score": float(similarities[index])
        })

    return results

load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)

def generate_answer(question, retrieved_chunks):
    context_parts = []

    for chunk in retrieved_chunks:
        context_parts.append(
            f"[Page {chunk['page']}]\n{chunk['text']}"
        )

    context = "\n\n".join(context_parts)

    prompt = f"""
You are answering questions based on a technical document.

Use only the context below.

If the answer cannot be found in the context, say:
"I could not find the answer in the document."

Context:
{context}

Question:
{question}

Answer clearly and include page references when possible.
"""

    response = client.responses.create(
        model="gpt-5-mini",
        input=prompt
    )

    return response.output_text

def ask_question(question, chunks, embeddings):
    retrieved_chunks = retrieve_top_k(
        question,
        chunks,
        embeddings,
        top_k=3
    )

    answer = generate_answer(
        question,
        retrieved_chunks
    )

    return answer, retrieved_chunks