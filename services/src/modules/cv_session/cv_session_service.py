from .dto.cv_session_dto import SessionDto
from sqlalchemy.ext.asyncio import AsyncSession
from .dto.cv_session_dto import SessionDto, SubmitToGetOtherQuestionsDto, OverallSummarizeDto
from src.utils.n8n_util import get_following_questions, post_data
from sqlalchemy import select, delete
from src.entities.cv_analysis_session_entity import CvAnalysisSessionEntity
from src.entities.question_entity import QuestionEntity
from datetime import datetime
from src.entities.skill_gap_entity import SessionSkillGapEntity
from src.entities.skill_gap_resource_type_entity import SkillGapResourceTypeEntity
from src.entities.article_recommendation_entity import ArticleRecommendationEntity
from sqlalchemy.orm import selectinload
from src.entities.session_keyword_entity import SessionKeywordEntity
from src.entities.answer_entity import AnswerEntity
from src.entities.question_entity import QuestionEntity

class CvSessionService: 
    def __init__(self):
        pass

    async def get_overall_summary_cv(self, data: OverallSummarizeDto, session: AsyncSession):

        json_data = {
            "session_id": data.session_id,
            "summary": data.summary,
            "questionsR1": data.questionsR1,
            "questionsR2": data.questionsR2,
            "answersR1": data.answersR1,
            "answersR2": data.answersR2,
        }


        overall_summary = post_data(data=json_data)

        print(overall_summary)

        return {
            "success": True
        }

    async def submit_first_answers_get_second_turns_questions(
        self,
        data: SubmitToGetOtherQuestionsDto,
        session: AsyncSession
    ):
        stmt = select(CvAnalysisSessionEntity).where(
            CvAnalysisSessionEntity.id == data.session_id
        )
        result = await session.execute(stmt)
        session_entity = result.scalar_one_or_none()

        if not session_entity:
            raise Exception("Session không tồn tại")

        stmt_questions = (
            select(QuestionEntity)
            .where(QuestionEntity.session_id == data.session_id)
            .order_by(QuestionEntity.order_index)
        )

        result_questions = await session.execute(stmt_questions)
        db_questions = result_questions.scalars().all()

        if len(db_questions) != len(data.answers):
            raise Exception("Số lượng answers không khớp với questions trong DB")

        for index, question_entity in enumerate(db_questions):
            answer_entity = AnswerEntity(
                question_id=question_entity.id,
                answer=data.answers[index],
            )
            session.add(answer_entity)

        await session.flush()  # đảm bảo insert xong trước khi gọi n8n

        payload = {
            "session_id": data.session_id,
            "questions": data.questions,
            "answers": data.answers
        }

        n8n_response = get_following_questions(payload)

        print(n8n_response)

        following_questions = n8n_response[0]["questions"]

        if not following_questions:
            raise Exception("n8n không trả về câu hỏi")

        # Xác định order_index tiếp theo
        current_max_index = max(q.order_index for q in db_questions)

        # Lưu câu hỏi vòng 2
        for i, content in enumerate(following_questions):
            question_entity = QuestionEntity(
                session_id=data.session_id,
                content=content,
                order_index=current_max_index + i + 1,
                created_at=datetime.utcnow()
            )
            session.add(question_entity)

        # Commit tất cả
        await session.commit()

        return {
            "message": "Submit thành công, đã lưu answers và tạo câu hỏi vòng 2",
            "questions": following_questions
        }
    
    async def getDetailSession(self, id: str, session: AsyncSession): 
        """
        Load session detail với tất cả relationships
        """
        result = await session.execute(
            select(CvAnalysisSessionEntity)
            .options(
                # Load questions
                selectinload(CvAnalysisSessionEntity.questions)
                    .selectinload(QuestionEntity.answer),
                
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
                selectinload(CvAnalysisSessionEntity.questions)
                    .selectinload(QuestionEntity.answer),
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
        session_entity.evaluate = data.evaluate
        session_entity.status = "DONE"
        session_entity.completed_at = datetime.utcnow()

        # 3. Clear old questions (cascade sẽ tự xóa answers)
        await session.execute(
            delete(QuestionEntity)
            .where(QuestionEntity.session_id == session_entity.id)
        )

        # Validate questions & answers length
        if len(data.questions) != len(data.answers):
            raise Exception("Questions and Answers length mismatch")

        # 4. Insert new questions + answers
        new_questions = []

        for index, (q_content, a_content) in enumerate(zip(data.questions, data.answers)):
            question = QuestionEntity(
                session_id=session_entity.id,
                content=q_content,
                order_index=index
            )

            # Tạo AnswerEntity gắn vào question
            question.answer = AnswerEntity(
                answer=a_content
            )

            new_questions.append(question)

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
