from fastapi import APIRouter, Depends
from src.interceptors.resonse_interceptor import InterceptRoute
from sqlalchemy.ext.asyncio import AsyncSession
from .dto.cv_session_dto import SessionDto, SubmitToGetOtherQuestionsDto, OverallSummarizeDto
from sqlalchemy.ext.asyncio import AsyncSession
from src.depends.depends import get_session
from .cv_session_service import CvSessionService
from pprint import pprint

router = APIRouter(prefix="/cv-session", tags=["CV Session"], route_class=InterceptRoute)

@router.post('/get-analysed-result')
async def get_analysed_result(data: SessionDto, session: AsyncSession = Depends(get_session)):
    service = CvSessionService()
    print(data)
    return await service.updateSession(session=session, data=data)
    

@router.get('/get-session-detail/{session_id}')
async def get_session_detail(session_id: str, session: AsyncSession = Depends(get_session)):
    service = CvSessionService()
    result = await service.getDetailSession(id=session_id, session=session)
    return {"success": True, "data": result}


@router.post("/submit-first-questions-get-other")
async def submit_first_answers_get_second_turns_questions(
    data: SubmitToGetOtherQuestionsDto,
    session: AsyncSession = Depends(get_session)
):
    service = CvSessionService()
    result = await service.submit_first_answers_get_second_turns_questions(data, session)
    return result

@router.post("/finallize")
async def finallize(data: OverallSummarizeDto, session: AsyncSession = Depends(get_session)):
    service = CvSessionService()
    result = await service.get_overall_summary_cv(data, session)
    return result