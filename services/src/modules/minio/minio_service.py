from fastapi import UploadFile
from src.utils.file_util import FileUtil
from src.config.minio_config import MinioConfig
from minio import Minio
from minio.error import S3Error
from typing import Optional
import os
from ...config.logger import logger

class MinioService:
    def __init__(self, util: FileUtil):
        self.util = util
        self.config = MinioConfig()
        self.client: Minio = self.config.get_client()
        self.bucket = self.config.bucket_name

    async def upload_file(
        self,
        file: UploadFile,
        folder: str = ""
    ) -> dict:
        """
        Upload file lên MinIO (handle UploadFile trực tiếp)
        """
        try:
            # Generate tên file unique
            new_filename = await self.util.generate_file_name(file.filename)

            object_name = (
                f"{folder}/{new_filename}"
                if folder else new_filename
            )

            # Seek lại đầu file (cực kỳ quan trọng)
            file.file.seek(0)

            self.client.put_object(
                bucket_name=self.bucket,
                object_name=object_name,
                data=file.file,
                length=-1,  # streaming mode
                part_size=10 * 1024 * 1024,  # 10MB
                content_type=file.content_type
            )

            return {
                "success": True,
                "filename": new_filename,
                "object_name": object_name,
                "content_type": file.content_type,
                "bucket": self.bucket
            }

        except S3Error as e:
            return {
                "success": False,
                "error": str(e)
            }

    async def download_file(self, object_name: str) -> Optional[bytes]:
        response = None
        try:
            response = self.client.get_object(self.bucket, object_name)
            return response.read()
        except S3Error as e:
            logger.error(f"MinIO error: {e}")
            return None
        except Exception as e:
            logger.error(f"Download failed: {e}")
            return None
        finally:
            if response:
                response.close()
                response.release_conn()

    async def delete_file(self, object_name: str) -> bool:
        try:
            self.client.remove_object(self.bucket, object_name)
            return True
        except S3Error:
            return False

    async def get_file_url(
        self,
        object_name: str,
        expires: int = 3600
    ) -> Optional[str]:
        try:
            from datetime import timedelta
            return self.client.presigned_get_object(
                self.bucket,
                object_name,
                expires=timedelta(seconds=expires)
            )
        except S3Error:
            return None
