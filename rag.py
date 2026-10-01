from pypdf import PdfReader
import re

def load_pdf(file):
    reader = PdfReader(file)
    pages = []
    for number, page in enumerate(reader.pages):
        text = page.extract_text()
        if text:
            pages.append({
                "text": text,
                "page_number": number + 1
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
import re

from pypdf import PdfReader


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