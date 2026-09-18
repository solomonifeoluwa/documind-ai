from pathlib import Path

from docx import Document as DocxDocument
from pypdf import PdfReader

class DocumentExtractor:
    @staticmethod
    def extract_text(
        file_path: str,
        content_type: str
    ) -> str:

        if content_type == "application/pdf":
            return DocumentExtractor._extract_pdf(file_path)

        if content_type == (
            "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        ):
            return DocumentExtractor._extract_docx(file_path)

        if content_type == "text/plain":
            return DocumentExtractor._extract_txt(file_path)

        raise ValueError("Unsupported document type.")

    @staticmethod
    def _extract_pdf(file_path: str) -> str:
        reader = PdfReader(file_path)

        text = []

        for page in reader.pages:
            page_text = page.extract_text()

            if page_text:
                text.append(page_text)

        return "\n".join(text).strip()

    @staticmethod
    def _extract_docx(file_path: str) -> str:
        document = DocxDocument(file_path)

        paragraphs = []

        for paragraph in document.paragraphs:
            if paragraph.text.strip():
                paragraphs.append(paragraph.text)

        return "\n".join(paragraphs).strip()

    @staticmethod
    def _extract_txt(file_path: str) -> str:
        return Path(file_path).read_text(
            encoding="utf-8"
        ).strip()