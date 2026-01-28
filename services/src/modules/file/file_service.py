from ..minio.minio_service import MinioService
from fastapi import HTTPException, UploadFile, status, Depends
from src.utils.file_util import FileUtil
from .file_scan_service import FileScanService
from ..formatter.cv_formatter import FlexibleCVParser
from src.utils.n8n_util import post_data
from sqlalchemy.ext.asyncio import AsyncSession
from src.entities.media_file_entity import MediaFileEntity
from src.entities.cv_analysis_session_entity import CvAnalysisSessionEntity
from src.depends.depends import get_session
from sqlalchemy import select

class FileService: 
    def __init__(self) -> None:
        self.minioService = MinioService(FileUtil())
        self.MAX_FILE_SIZE = 5 * 1024 * 1024
        self.CHUNK_SIZE = 1024 * 1024 
        self.fileScanService = FileScanService()
        self.util = FileUtil()
        self.cvFormatter = FlexibleCVParser()

    async def upload_file(self, file: UploadFile, session: AsyncSession):
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

        upload_filed = await self.minioService.upload_file(
            file=file,
            folder=""
        )

        # CREATE NEW FILE AND RETURN SESSION ID
        new_data_file = MediaFileEntity(
            name=upload_filed["object_name"],      # ← Đổi từ .object_name
            link=upload_filed["bucket"],               # ← Đổi từ .bucket
            type=upload_filed["content_type"]          # ← Đổi từ .content_type
        )

        session.add(new_data_file)
        await session.commit()
        # await session.refresh(new_data_file)
        print("new file", new_data_file)

        return upload_filed 

    async def upload_multiple_files(self, files: list[UploadFile]):
        results = []

        for file in files:
            result = await self.minioService.upload_file(
                file=file,
                folder=""
            )
            results.append(result)

        return results

    async def get_data_from_cv(self, object_name: str, session: AsyncSession):
        file_bytes = await self.minioService.download_file(object_name)
        if not file_bytes:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="CV file not found"
            )
        
        text = await self.fileScanService.extract_text(
            file_bytes=file_bytes,
            filename=object_name
        )

        # FIND FILE ID
        dataFile = await session.scalar(
            select(MediaFileEntity)
            .where(MediaFileEntity.name == object_name)
        )

        # CREATE NEW SESSION
        new_session = CvAnalysisSessionEntity(
            cv_file_id= dataFile.id
        )
        session.add(new_session)
        await session.commit()
        await session.refresh(new_session)

        print("new_session", new_session.id)

        n8nData = {
            "summary": text,
            "session_id": str(new_session.id)
        }

        print("data to post", n8nData)

        post_data(n8nData)

        return {
            "object_name": object_name,
            "raw_text": text,
            "counts": len(text),
            "session_id": str(new_session.id)
        }