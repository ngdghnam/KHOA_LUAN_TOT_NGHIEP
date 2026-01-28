from fastapi import APIRouter, Depends
from .dto.request_dto import RequestCrawlDto, MultipleKeywordsDto, UrlDto
from .search_service import SearchService
from src.interceptors.resonse_interceptor import InterceptRoute
from sqlalchemy.ext.asyncio import AsyncSession
from src.depends.depends import get_session
from src.config.search import SearchingGoogle 
from src.utils.crawl_util import CrawlUtils

router = APIRouter(
    prefix="/search",
    tags=["Search"]
)

@router.post("/crawl-url")
async def crawlFromSpecificURL(data: UrlDto, session: AsyncSession = Depends(get_session)):
    search = SearchingGoogle()
    crawlUtils = CrawlUtils()    
    searchService = SearchService(search, crawlUtils, session)
    return await searchService.crawlFromSpecificURL(data)

@router.post("/crawl")
async def crawlData(request: RequestCrawlDto, session: AsyncSession = Depends(get_session)):
    search = SearchingGoogle()
    crawlUtils = CrawlUtils()    
    searchService = SearchService(search, crawlUtils, session)
    return await searchService.crawlData(request)

@router.post("/search-multiple")
async def crawlMultipleData(request: MultipleKeywordsDto, session: AsyncSession = Depends(get_session)):
    search = SearchingGoogle()
    crawlUtils = CrawlUtils()    
    searchService = SearchService(search, crawlUtils, session)
    return await searchService.crawlMultipleData(request)