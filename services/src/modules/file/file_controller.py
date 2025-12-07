from fastapi import APIRouter, UploadFile, File
from .file_service import FileService
from src.interceptors.resonse_interceptor import InterceptRoute

router = APIRouter(prefix="/files", tags=["files"], route_class=InterceptRoute)
service = FileService()

@router.post("/upload")
async def upload_file(
    file: UploadFile = File(...)
):
    return await service.upload_file(file)


@router.post("/upload-multiple")
async def upload_multiple_files(
    files: list[UploadFile] = File(...)
):
    return await service.upload_multiple_files(files)