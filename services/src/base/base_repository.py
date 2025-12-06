from abc import ABC, abstractmethod
from dataclasses import dataclass
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete, func, and_, insert
from sqlalchemy.orm import selectinload
from typing import TypeVar, Generic, List, Optional, Tuple, Any, Dict
from .options import *

T = TypeVar('T')

class BaseRepository(ABC, Generic[T]):
    def __init__(self, model: type[T], session: AsyncSession) -> None:
        self.model = model
        self.session = session

    #region CRUD    
    async def create(self, data: Dict[str, Any]) -> T:
        entity = self.model(**data)
        self.session.add(entity)
        await self.session.commit()
        await self.session.refresh(entity)
        return entity

    async def insert(self, data: Dict[str, Any]) -> T:
        stmt = insert(self.model).values(**data).returning(self.model)
        result = await self.session.execute(stmt)
        await self.session.commit()
        entity = result.scalar_one()
        return entity

    async def delete(self, id: str):
        stmt = delete(self.model).where(self.model.id == id)
        result = await self.session.execute(stmt)
        await self.session.commit()
        return result.rowcount > 0

    async def update(self, id: str, data: Dict[str, Any]):
        stmt = (
            update(self.model)
            .where(self.model.id == id)
            .values(**data)
            .execution_options(synchronize_session="fetch")
        )
        result = await self.session.execute(stmt)
        await self.session.commit()
        
        if result.rowcount > 0:
            return await self.findOne({'where': {'id': id}})
        return None
    
    async def save(self, entity: T) -> T:
        self.session.add(entity)
        await self.session.commit()
        await self.session.refresh(entity)
        return entity
    #endregion

    #region Find and Pagination
    async def findOne(self, options: Options) -> Optional[T]:
        stmt = select(self.model)

        # Apply select (specific columns)
        if 'select' in options and options['select']:
            columns = [getattr(self.model, col) for col in options['select'] if hasattr(self.model, col)]
            if columns:
                stmt = select(*columns)
        
        # Apply where conditions
        if 'where' in options and options['where']:
            conditions = self._build_where_conditions(options['where'])
            if conditions:
                stmt = stmt.where(and_(*conditions))
        
        # Apply eager loading for relations
        if 'relations' in options and options['relations']:
            for relation in options['relations']:
                if hasattr(self.model, relation):
                    stmt = stmt.options(selectinload(getattr(self.model, relation)))
        
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def findAndCount(self, options: FindOptions) -> Tuple[List[T], int]:
        # Apply select (specific columns)
        if 'select' in options and options['select']:
            columns = [getattr(self.model, col) for col in options['select'] if hasattr(self.model, col)]
            if columns:
                stmt = select(*columns)

        # Apply where conditions
        if 'where' in options and options['where']:
            conditions = self._build_where_conditions(options['where'])
            if conditions:
                where_clause = and_(*conditions)
                stmt = stmt.where(where_clause)
                count_stmt = count_stmt.where(where_clause)
        
        # Get total count
        count_result = await self.session.execute(count_stmt)
        total = count_result.scalar()
        
        # Apply relations
        if 'relations' in options and options['relations']:
            for relation in options['relations']:
                if hasattr(self.model, relation):
                    stmt = stmt.options(selectinload(getattr(self.model, relation)))
        
        # Apply ordering
        if 'order' in options and options['order']:
            for field, direction in options['order'].items():
                if hasattr(self.model, field):
                    column = getattr(self.model, field)
                    stmt = stmt.order_by(
                        column.desc() if direction.upper() == 'DESC' else column.asc()
                    )
        
        # Apply pagination
        if 'skip' in options and options['skip']:
            stmt = stmt.offset(options['skip'])
        if 'take' in options and options['take']:
            stmt = stmt.limit(options['take'])
        
        result = await self.session.execute(stmt)
        entities = result.scalars().all()
        
        return list(entities), total
    
    async def find(self, options: FindOptions) -> List[T]:
        stmt = select(self.model)
        
        # Apply select (specific columns)
        if 'select' in options and options['select']:
            columns = [getattr(self.model, col) for col in options['select'] if hasattr(self.model, col)]
            if columns:
                stmt = select(*columns)
        
        # Apply where conditions
        if 'where' in options and options['where']:
            conditions = self._build_where_conditions(options['where'])
            if conditions:
                stmt = stmt.where(and_(*conditions))
        
        # Apply relations
        if 'relations' in options and options['relations']:
            for relation in options['relations']:
                if hasattr(self.model, relation):
                    stmt = stmt.options(selectinload(getattr(self.model, relation)))
        
        # Apply ordering
        if 'order' in options and options['order']:
            for field, direction in options['order'].items():
                if hasattr(self.model, field):
                    column = getattr(self.model, field)
                    stmt = stmt.order_by(
                        column.desc() if direction.upper() == 'DESC' else column.asc()
                    )
        
        # Apply pagination
        if 'skip' in options and options['skip']:
            stmt = stmt.offset(options['skip'])
        if 'take' in options and options['take']:
            stmt = stmt.limit(options['take'])
        
        result = await self.session.execute(stmt)
        return list(result.scalars().all())
    #endregion

