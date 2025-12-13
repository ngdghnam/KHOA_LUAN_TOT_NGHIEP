from ..minio.minio_service import MinioService
from fastapi import HTTPException, UploadFile, status
from src.utils.file_util import FileUtil
from .file_scan_service import FileScanService

class FileService: 
    def __init__(self) -> None:
        self.minioService = MinioService(FileUtil())
        self.MAX_FILE_SIZE = 5 * 1024 * 1024
        self.CHUNK_SIZE = 1024 * 1024 
        self.fileScanService = FileScanService()
        self.util = FileUtil()

    async def upload_file(self, file: UploadFile):
        total_size = 0

        while True:
            chunk = await file.read(self.CHUNK_SIZE)
            if not chunk:
                break

            total_size += len(chunk)
            if total_size > self.MAX_FILE_SIZE:
                raise HTTPException(
                    status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                    detail="File size exceeds 5MB limit"
                )

        # Reset pointer về đầu file
        await file.seek(0)

        return await self.minioService.upload_file(
            file=file,
            folder=""
        )

    async def upload_multiple_files(self, files: list[UploadFile]):
        results = []

        for file in files:
            result = await self.minioService.upload_file(
                file=file,
                folder=""
            )
            results.append(result)

        return results

    async def get_data_from_cv(self, object_name: str):
        file_bytes = await self.minioService.download_file(object_name)
        if not file_bytes:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="CV file not found"
            )
        
        try:
            text = await self.fileScanService.extract_text(
                file_bytes=file_bytes,
                filename=object_name
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=f"Cannot read CV file: {str(e)}"
            )
        
        try:
            parsed_data = await self.fileScanService.parse(text)
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Cannot parse CV data: {str(e)}"
            )

        return {
            "object_name": object_name,
            "raw_text": text,
            "counts": len(text)
        }