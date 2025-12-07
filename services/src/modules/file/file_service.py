from ..minio.minio_service import MinioService
from fastapi import UploadFile  
from src.utils.file_util import FileUtil

class FileService: 
    def __init__(self) -> None:
        self.minioService = MinioService(FileUtil())

    async def upload_file(self, file: UploadFile):
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

    async def extractPdfFile(self):
        return   