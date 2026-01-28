from .dto.cv_session_dto import SessionDto
from sqlalchemy.ext.asyncio import AsyncSession
from .dto.cv_session_dto import SessionDto
from src.utils.n8n_util import post_data
from sqlalchemy import select, delete
from src.entities.cv_analysis_session_entity import CvAnalysisSessionEntity
from src.entities.question_entity import QuestionEntity
from datetime import datetime
from src.entities.skill_gap_entity import SessionSkillGapEntity
from src.entities.skill_gap_resource_type_entity import SkillGapResourceTypeEntity
from src.entities.article_recommendation_entity import ArticleRecommendationEntity
from sqlalchemy.orm import selectinload
from src.entities.session_keyword_entity import SessionKeywordEntity


class CvSessionService: 
    def __init__(self):
        pass
    
    async def getDetailSession(self, id: str, session: AsyncSession): 
        """
        Load session detail với tất cả relationships
        """
        result = await session.execute(
            select(CvAnalysisSessionEntity)
            .options(
                # Load questions
                selectinload(CvAnalysisSessionEntity.questions),
                
                # Load skill gaps và resource types của nó
                selectinload(CvAnalysisSessionEntity.skill_gaps)
                    .selectinload(SessionSkillGapEntity.resource_types),
                
                # Load article recommendations
                selectinload(CvAnalysisSessionEntity.article_recommendations),

                # Load keywords
                selectinload(CvAnalysisSessionEntity.keywords)
            )
            .where(CvAnalysisSessionEntity.id == id)
        )
    
        session_entity = result.scalar_one_or_none()
        
        if not session_entity:
            raise Exception(f"Session not found: {id}")
        
        return session_entity
        

    async def updateSession(self, session: AsyncSession, data: SessionDto):
        # 1. Load session entity với eager loading
        result = await session.execute(
            select(CvAnalysisSessionEntity)
            .options(
                selectinload(CvAnalysisSessionEntity.questions),
                selectinload(CvAnalysisSessionEntity.skill_gaps)
                    .selectinload(SessionSkillGapEntity.resource_types),
                selectinload(CvAnalysisSessionEntity.article_recommendations),
                selectinload(CvAnalysisSessionEntity.keywords)
            )
            .where(CvAnalysisSessionEntity.id == data.session_id)
        )
        session_entity = result.scalar_one_or_none()

        if not session_entity:
            raise Exception(f"Session not found: {data.session_id}")
        
        # 1.1. Update keywords
        session_entity.keywords.clear()

        # Add keywords mới
        for kw in data.keywords:
            session_entity.keywords.append(
                SessionKeywordEntity(
                    name=kw,
                    session_id=session_entity.id
                )
            )


        # 2. Update fields đơn giản
        session_entity.summary = data.summary
        session_entity.status = "DONE"
        session_entity.completed_at = datetime.utcnow()

        # 3. Clear old questions
        await session.execute(
            delete(QuestionEntity)
            .where(QuestionEntity.session_id == session_entity.id)
        )

        # 4. Insert new questions (tạo mới, không gán qua relationship)
        new_questions = [
            QuestionEntity(
                session_id=session_entity.id,  # ← Thêm session_id trực tiếp
                content=q,
                order_index=index
            )
            for index, q in enumerate(data.questions)
        ]
        session.add_all(new_questions)

        # 5. Clear old skill gaps
        await session.execute(
            delete(SessionSkillGapEntity)
            .where(SessionSkillGapEntity.session_id == session_entity.id)
        )

        # 6. Insert new skill gaps
        new_skill_gaps = [
            SessionSkillGapEntity(
                session_id=session_entity.id,  # ← Thêm session_id trực tiếp
                learning_keyword=sg.learning_keyword,
                skill_gap=sg.skill_gap,
                why_it_matters=sg.why_it_matters,
                resource_types=[
                    SkillGapResourceTypeEntity(resource_type=r)
                    for r in sg.resource_types
                ]
            )
            for sg in data.skill_gaps
        ]
        session.add_all(new_skill_gaps)

        # 7. Clear old articles
        await session.execute(
            delete(ArticleRecommendationEntity)
            .where(ArticleRecommendationEntity.session_id == session_entity.id)
        )

        # 8. Insert new articles
        new_articles = [
            ArticleRecommendationEntity(
                session_id=session_entity.id,  # ← Thêm session_id trực tiếp
                title=a.title,
                url=a.url,
                # content=a.content,
                # snippet=a.snippet
            )
            for a in data.articles
        ]
        session.add_all(new_articles)

        # 9. Commit
        await session.commit()
        await session.refresh(session_entity)

        return {"success": True}
