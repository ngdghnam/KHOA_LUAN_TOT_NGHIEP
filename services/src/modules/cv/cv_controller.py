from fastapi import APIRouter, Depends
from .cv_service import CvService
from src.interceptors.resonse_interceptor import InterceptRoute
from sqlalchemy.ext.asyncio import AsyncSession
from src.depends.depends import get_session

router = APIRouter(prefix="/users", tags=["users"], route_class=InterceptRoute)

@router.post("/scan-cv")
async def scan_cv(session: AsyncSession = Depends(get_session)):
    service: CvService = CvService()