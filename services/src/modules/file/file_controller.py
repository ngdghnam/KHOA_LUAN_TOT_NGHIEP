from fastapi import APIRouter, UploadFile, File
from .file_service import FileService
from .file_scan_service import FileScanService
from src.interceptors.resonse_interceptor import InterceptRoute
from .dto.scanned_cv_dto import ScannedCvDto

router = APIRouter(prefix="/files", tags=["files"], route_class=InterceptRoute)
service = FileService()
scan_service = FileScanService()

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

@router.post("/scan-cv")
async def scan_cv(data: ScannedCvDto):
    return await service.get_data_from_cv(object_name=data.cv_name)