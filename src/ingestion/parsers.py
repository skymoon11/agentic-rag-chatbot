import os
import uuid

import pandas as pd
from docx import Document
from pypdf import PdfReader

from src.ingestion.audio_service import transcribe_audio

AUDIO_EXTENSIONS = {".mp3", ".wav", ".m4a", ".ogg"}


def parse_pdf(file_path: str) -> str:
    reader = PdfReader(file_path)
    text = ""
    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text + "\n"
    return text


def parse_docx(file_path: str) -> str:
    doc = Document(file_path)
    return "\n".join([paragraph.text for paragraph in doc.paragraphs if paragraph.text])


def parse_csv(file_path: str) -> str:
    dataframe = pd.read_csv(file_path)
    # Convert tabular records to plain text representations.
    return dataframe.to_string(index=False)


def parse_txt(file_path: str) -> str:
    with open(file_path, "r", encoding="utf-8", errors="ignore") as file:
        return file.read()


def process_file(uploaded_file, upload_dir: str = "./data/uploads") -> dict:
    """Parse supported file formats and return text content with metadata."""
    os.makedirs(upload_dir, exist_ok=True)
    filename = uploaded_file.filename
    extension = os.path.splitext(filename)[1].lower()
    save_path = os.path.join(upload_dir, filename)
    uploaded_file.save(save_path)

    document_id = str(uuid.uuid4())

    if extension == ".pdf":
        content = parse_pdf(save_path)
    elif extension in [".docx", ".doc"]:
        content = parse_docx(save_path)
    elif extension == ".csv":
        content = parse_csv(save_path)
    elif extension == ".txt":
        content = parse_txt(save_path)
    elif extension in AUDIO_EXTENSIONS:
        content = transcribe_audio(save_path)
    else:
        raise ValueError(f"Unsupported file format: {extension}")

    return {
        "document_id": document_id,
        "filename": filename,
        "format": extension,
        "char_count": len(content),
        "text_content": content,
    }