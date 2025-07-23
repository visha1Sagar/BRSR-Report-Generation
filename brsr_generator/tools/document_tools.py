import os
from typing import Optional

try:
    from docx import Document as DocxDocument
except ImportError:
    DocxDocument = None
try:
    import PyPDF2
except ImportError:
    PyPDF2 = None
try:
    import openpyxl
except ImportError:
    openpyxl = None

import csv


def load_document(file_path: str) -> Optional[str]:
    """
    Load a document (Word, PDF, Excel, CSV, or plain text) and return its text content as a string.
    """
    ext = os.path.splitext(file_path)[1].lower()
    if ext == '.docx':
        if DocxDocument is None:
            raise ImportError("python-docx is required for .docx files.")
        doc = DocxDocument(file_path)
        return '\n'.join([para.text for para in doc.paragraphs])
    elif ext == '.pdf':
        if PyPDF2 is None:
            raise ImportError("PyPDF2 is required for .pdf files.")
        with open(file_path, 'rb') as f:
            reader = PyPDF2.PdfReader(f)
            text = []
            for page in reader.pages:
                text.append(page.extract_text() or "")
            return '\n'.join(text)
    elif ext in ('.xlsx', '.xls'):
        if openpyxl is None:
            raise ImportError("openpyxl is required for Excel files.")
        wb = openpyxl.load_workbook(file_path, data_only=True)
        text = []
        for ws in wb.worksheets:
            for row in ws.iter_rows(values_only=True):
                text.append('\t'.join([str(cell) if cell is not None else '' for cell in row]))
        return '\n'.join(text)
    elif ext == '.csv':
        with open(file_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)
            text = ['\t'.join(row) for row in reader]
        return '\n'.join(text)
    elif ext == '.txt':
        with open(file_path, encoding='utf-8') as f:
            return f.read()
    else:
        raise NotImplementedError(f"Unsupported file type: {ext}")

def save_document(document: object, file_path: str) -> None:
    """
    Save a document object to the specified file path. (Stub for now)
    """
    # TODO: Implement document saving logic for various formats
    pass 