from io import BytesIO
from PIL import Image
import fitz
import pytesseract
from docx import Document
from pathlib import Path
import re
import asyncio

class FileScanService: 
    def __init__(self):
        pass

    async def extract_text(self, file_bytes: bytes, filename: str) -> str:
        """
        Extract text từ file (async version để không block event loop)
        """
        ext = Path(filename).suffix.lower()

        # Chạy extraction trong thread pool vì là blocking operation
        loop = asyncio.get_event_loop()
        
        if ext == ".pdf":
            return await loop.run_in_executor(None, self._read_pdf, file_bytes)
        elif ext == ".docx":
            return await loop.run_in_executor(None, self._read_docx, file_bytes)
        elif ext in [".png", ".jpg", ".jpeg"]:
            return await loop.run_in_executor(None, self._read_image, file_bytes)
        else:
            raise ValueError(f"Unsupported file format: {ext}")

    def _read_pdf(self, file_bytes: bytes) -> str:
        doc = fitz.open(stream=file_bytes, filetype="pdf")
        return "\n".join(page.get_text() for page in doc)

    def _read_docx(self, file_bytes: bytes) -> str:
        doc = Document(BytesIO(file_bytes))
        return "\n".join(p.text for p in doc.paragraphs)

    def _read_image(self, file_bytes: bytes) -> str:
        image = Image.open(BytesIO(file_bytes))
        return pytesseract.image_to_string(image)
    
    async def parse(self, text: str) -> dict:
        email = re.findall(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+", text)
        phone = re.findall(r"(0|\+84)[0-9]{9}", text)

        return {
            "email": email[0] if email else None,
            "phone": phone[0] if phone else None,
            "raw_text_length": len(text)
        }