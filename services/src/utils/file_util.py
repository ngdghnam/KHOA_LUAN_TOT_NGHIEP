import uuid
from datetime import datetime
from pathlib import Path

class FileUtil:
    async def generate_file_name(self, original_filename: str) -> str:
        """
        Tạo tên file unique từ tên file gốc
        Format: timestamp_uuid_original_name.ext
        """
        # Lấy extension
        file_path = Path(original_filename)
        extension = file_path.suffix
        name_without_ext = file_path.stem
        
        # Tạo tên file unique
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        unique_id = str(uuid.uuid4())[:8]
        
        new_filename = f"{timestamp}_{unique_id}_{name_without_ext}{extension}"
        return new_filename
    
    def get_content_type(self, filename: str) -> str:
        """Xác định content type dựa trên extension"""
        extension = Path(filename).suffix.lower()
        
        content_types = {
            '.jpg': 'image/jpeg',
            '.jpeg': 'image/jpeg',
            '.png': 'image/png',
            '.gif': 'image/gif',
            '.pdf': 'application/pdf',
            '.doc': 'application/msword',
            '.docx': 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
            '.xls': 'application/vnd.ms-excel',
            '.xlsx': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            '.txt': 'text/plain',
            '.zip': 'application/zip',
        }
        
        return content_types.get(extension, 'application/octet-stream')