from minio import Minio
from minio.error import S3Error

class MinioConfig: 
    def __init__(self):
        pass

    def connect(self): 
        client = Minio(
            endpoint="",
            access_key="",
            secret_key="",
        )