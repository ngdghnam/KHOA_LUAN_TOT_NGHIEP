from sqlalchemy.ext.asyncio import AsyncSession

class CvService: 
    def __init__(self, session: AsyncSession):
        self.session = session