from minio import Minio
from minio.error import S3Error
from .environments import settings

class MinioConfig: 
    def __init__(self):
        self.client = None
        self.bucket_name = settings.MINIO_BUCKET

    def connect(self) -> Minio:
        """Kết nối tới MinIO server"""
        try:
            self.client = Minio(
                endpoint=settings.MINIO_ENDPOINT,
                access_key=settings.MINIO_ROOT_USER,
                secret_key=settings.MINIO_ROOT_PASSWORD,
                secure=False
            )
            
            # Tạo bucket nếu chưa tồn tại
            if not self.client.bucket_exists(self.bucket_name):
                self.client.make_bucket(self.bucket_name)
            
            return self.client
        except S3Error as e:
            print(f"Lỗi kết nối MinIO: {e}")
            raise
    
    def get_client(self) -> Minio:
        """Lấy MinIO client"""
        if self.client is None:
            self.connect()
        return self.client

minio_config = MinioConfig()