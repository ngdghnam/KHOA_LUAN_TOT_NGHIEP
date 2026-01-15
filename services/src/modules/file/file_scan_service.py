from io import BytesIO
from PIL import Image
import fitz
import pytesseract
from docx import Document
from pathlib import Path
import re
import asyncio
from pdf2image import convert_from_bytes

class FileScanService: 
    def __init__(self):
        # pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
        self._check_tesseract()

    def _check_tesseract(self):
        """Kiểm tra xem Tesseract có được cài đặt không"""
        try:
            pytesseract.get_tesseract_version()
        except Exception as e:
            raise RuntimeError(
                "Tesseract OCR is not installed or not in PATH. "
                "Please install it:\n"
                "- Windows: https://github.com/UB-Mannheim/tesseract/wiki\n"
                "- Linux: sudo apt-get install tesseract-ocr\n"
                "- macOS: brew install tesseract"
            )

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
        text = "\n".join(page.get_text() for page in doc)

        #Fix spacing issues
        text = self._fix_spacing(text)
        
        # Nếu text vẫn kém → OCR
        if self._is_poor_quality_text(text):
            return self._ocr_pdf(file_bytes)

        return text
    
    def _ocr_pdf(self, file_bytes: bytes) -> str:
        images = convert_from_bytes(file_bytes, dpi=300)
        text = ""
        for img in images:
            # OCR trực tiếp từ PIL Image, không cần convert sang bytes
            text += pytesseract.image_to_string(img)
        return text
    
    def _fix_spacing(self, text: str) -> str:
        """Fix words stuck together like 'ableto' → 'able to'"""
        text = re.sub(r'([a-z])([A-Z])', r'\1 \2', text)
        return text
    
    def _is_poor_quality_text(self, text: str) -> bool:
        """Detect if extracted text is poor quality"""
        if len(text.strip()) < 50:
            return True
        
        words = text.split()
        if not words:
            return True
        
        # Quá nhiều từ dài (>25 chars) = text bị dính
        long_words = sum(1 for w in words if len(w) > 25)
        if long_words / len(words) > 0.03:  # >3%
            return True
        
        return False

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