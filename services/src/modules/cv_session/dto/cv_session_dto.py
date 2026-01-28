from pydantic import BaseModel, Field, EmailStr, HttpUrl
from typing import Optional, List

class ArticleDto(BaseModel): 
    title: str
    url: str
    content: str
    snippet: Optional[str] = ""

class SkillGapDto(BaseModel):
    learning_keyword: str
    skill_gap: str 
    resource_types: List[str]
    why_it_matters: str


class SessionDto(BaseModel):
    keywords: List[str]
    articles: List[ArticleDto]
    questions: List[str]
    total_articles: int
    summary: str
    skill_gaps: List[SkillGapDto]
    session_id: str

class UrlDto(BaseModel):
    """DTO for URL references (portfolio, LinkedIn, etc.)"""
    url: HttpUrl = Field(..., description="Valid URL")
    name: Optional[str] = Field(None, description="Display name for the URL", max_length=100)

    class Config:
        json_schema_extra = {
            "example": {
                "url": "https://linkedin.com/in/johndoe",
                "name": "LinkedIn Profile"
            }
        }

class CvSessionDto(BaseModel):
    """DTO representing a CV analysis session"""
    
    # Required fields
    name: str = Field(..., min_length=1, max_length=200, description="Candidate's full name")
    email: str = Field(..., description="Candidate's email address")
    cv_name: str = Field(..., min_length=1, max_length=255, description="Name/title of the CV file")
    position_applied: str = Field(..., min_length=1, max_length=200, description="Job position applied for")
    
    # Optional contact information
    phone_number: Optional[str] = Field(
        None, 
        pattern=r'^\+?[1-9]\d{1,14}$',  # E.164 format
        description="Phone number in international format"
    )
    
    # Professional information
    urls: Optional[list[UrlDto]] = Field(
        default=None,
        description="List of URLs (LinkedIn, portfolio, GitHub, etc.)",
        max_length=10
    )
    skills: Optional[list[str]] = Field(
        default=None,
        description="List of candidate's skills",
        max_length=50
    )
    experience_years: Optional[int] = Field(
        None,
        ge=0,
        le=70,
        description="Years of professional experience"
    )
    education_level: Optional[str] = Field(
        None,
        description="Highest education level achieved"
    )
    
    # Achievements
    awards: Optional[list[str]] = Field(
        default=None,
        description="List of awards and recognitions",
        max_length=20
    )
    certifications: Optional[list[str]] = Field(
        default=None,
        description="List of professional certifications",
        max_length=30
    )
    
    # Analysis results
    format_issues: Optional[list[str]] = Field(
        default=None,
        description="List of formatting issues found in the CV",
        max_length=50
    )
    weaknesses: Optional[list[str]] = Field(
        default=None,
        description="Identified weaknesses in the CV",
        max_length=30
    )
    strengths: Optional[list[str]] = Field(
        default=None,
        description="Identified strengths in the CV",
        max_length=30
    )

    class Config:
        json_schema_extra = {
            "example": {
                "name": "John Doe",
                "email": "john.doe@example.com",
                "cv_name": "John_Doe_Software_Engineer_2025.pdf",
                "position_applied": "Senior Software Engineer",
                "phone_number": "+84123456789",
                "urls": [
                    {"url": "https://linkedin.com/in/johndoe", "name": "LinkedIn"},
                    {"url": "https://github.com/johndoe", "name": "GitHub"}
                ],
                "skills": ["Python", "FastAPI", "PostgreSQL", "Docker"],
                "experience_years": 5,
                "education_level": "bachelor",
                "certifications": ["AWS Certified Developer"],
                "strengths": ["Strong technical skills", "Good communication"],
                "weaknesses": ["Limited leadership experience"],
                "format_issues": ["Inconsistent date formats"]
            }
        }