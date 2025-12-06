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
    async def findOne(self, options: Optional[Options] = None) -> Optional[T | Dict[str, Any]]:
        if options is None:
            options = {}

        has_select = 'select' in options and options['select']
        has_relations = 'relations' in options and options['relations']

        # Case 1: Has select (with or without relations)
        if has_select:
            return await self._findOne_with_select(options)
        
        # Case 2: No select, has relations
        if has_relations:
            return await self._findOne_with_relations(options)
        
        # Case 3: No select, no relations (simple query)
        return await self._findOne_simple(options)

    async def _findOne_simple(self, options: Dict) -> Optional[T]:
        """Simple findOne without select or relations"""
        stmt = select(self.model)
        
        if options.get('where'):
            conditions = self._build_where_conditions(options['where'])
            if conditions:
                stmt = stmt.where(and_(*conditions))
        
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def _findOne_with_relations(self, options: Dict) -> Optional[T]:
        """FindOne with relations but no select"""
        stmt = select(self.model)
        
        if options.get('where'):
            conditions = self._build_where_conditions(options['where'])
            if conditions:
                stmt = stmt.where(and_(*conditions))
        
        # Apply deep relations
        stmt = self._apply_relations(stmt, options['relations'])
        
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def _findOne_with_select(self, options: Dict) -> Optional[Dict[str, Any]]:
        """FindOne with select (may include relations)"""
        has_relations = options.get('relations')
        
        if has_relations:
            # When both select and relations exist, fetch full entity first
            entity = await self._findOne_with_relations(options)
            if entity is None:
                return None
            
            # Then extract selected fields
            result = {}
            for field in options['select']:
                if '.' in field:
                    # Handle nested fields like 'profile.name'
                    value = self._get_nested_value(entity, field)
                    result[field] = value
                elif hasattr(entity, field):
                    result[field] = getattr(entity, field)
            
            return result
        else:
            # Select without relations - direct column selection
            columns = [
                getattr(self.model, col) 
                for col in options['select'] 
                if hasattr(self.model, col)
            ]
            
            if not columns:
                return None
            
            stmt = select(*columns)
            
            if options.get('where'):
                conditions = self._build_where_conditions(options['where'])
                if conditions:
                    stmt = stmt.where(and_(*conditions))
            
            result = await self.session.execute(stmt)
            row = result.first()
            
            if row is None:
                return None
            
            return {col: row[i] for i, col in enumerate(options['select'])}

    async def find(self, options: Optional[FindOptions] = None) -> List[T | Dict[str, Any]]:
        if options is None:
            options = {}

        has_select = options.get('select')
        has_relations = options.get('relations')

        # Case 1: Has select
        if has_select:
            return await self._find_with_select(options)
        
        # Case 2: No select, has relations
        if has_relations:
            return await self._find_with_relations(options)
        
        # Case 3: Simple query
        return await self._find_simple(options)

    async def _find_simple(self, options: Dict) -> List[T]:
        stmt = select(self.model)
        
        if options.get('where'):
            conditions = self._build_where_conditions(options['where'])
            if conditions:
                stmt = stmt.where(and_(*conditions))
        
        stmt = self._apply_ordering(stmt, options)
        stmt = self._apply_pagination(stmt, options)
        
        result = await self.session.execute(stmt)
        return list(result.scalars().all())

    async def _find_with_relations(self, options: Dict) -> List[T]:
        """Find with relations but no select"""
        stmt = select(self.model)
        
        if options.get('where'):
            conditions = self._build_where_conditions(options['where'])
            if conditions:
                stmt = stmt.where(and_(*conditions))
        
        stmt = self._apply_relations(stmt, options['relations'])
        stmt = self._apply_ordering(stmt, options)
        stmt = self._apply_pagination(stmt, options)
        
        result = await self.session.execute(stmt)
        return list(result.scalars().all())

    async def _find_with_select(self, options: Dict) -> List[Dict[str, Any]]:
        has_relations = options.get('relations')
        
        if has_relations:
            # Fetch full entities with relations
            entities = await self._find_with_relations(options)
            
            # Extract selected fields from each entity
            results = []
            for entity in entities:
                row_data = {}
                for field in options['select']:
                    if '.' in field:
                        value = self._get_nested_value(entity, field)
                        row_data[field] = value
                    elif hasattr(entity, field):
                        row_data[field] = getattr(entity, field)
                results.append(row_data)
            
            return results
        else:
            # Direct column selection without relations
            columns = [
                getattr(self.model, col) 
                for col in options['select'] 
                if hasattr(self.model, col)
            ]
            
            if not columns:
                return []
            
            stmt = select(*columns)
            
            if options.get('where'):
                conditions = self._build_where_conditions(options['where'])
                if conditions:
                    stmt = stmt.where(and_(*conditions))
            
            stmt = self._apply_ordering(stmt, options)
            stmt = self._apply_pagination(stmt, options)
            
            result = await self.session.execute(stmt)
            rows = result.all()
            
            return [
                {col: row[i] for i, col in enumerate(options['select'])}
                for row in rows
            ]

    async def findAndCount(self, options: Optional[FindOptions] = None) -> Tuple[List[T | Dict[str, Any]], int]:
        if options is None:
            options = {}

        # Get count
        count_stmt = select(func.count()).select_from(self.model)
        
        if options.get('where'):
            conditions = self._build_where_conditions(options['where'])
            if conditions:
                count_stmt = count_stmt.where(and_(*conditions))
        
        count_result = await self.session.execute(count_stmt)
        total = count_result.scalar()
        
        # Get entities using find (which handles all cases)
        entities = await self.find(options)
        
        return entities, total
    
    #endregion

    #region Helper Methods
    def _build_where_conditions(self, where: Dict[str, Any]) -> List[Any]:
        """
        Build SQLAlchemy where conditions from a dictionary.
        Supports basic operators and nested conditions.
        """
        conditions = []
        
        for field, value in where.items():
            if not hasattr(self.model, field):
                continue
                
            column = getattr(self.model, field)
            
            # Handle dictionary values with operators
            if isinstance(value, dict):
                for operator, operand in value.items():
                    if operator == 'eq' or operator == '==':
                        conditions.append(column == operand)
                    elif operator == 'ne' or operator == '!=':
                        conditions.append(column != operand)
                    elif operator == 'gt' or operator == '>':
                        conditions.append(column > operand)
                    elif operator == 'gte' or operator == '>=':
                        conditions.append(column >= operand)
                    elif operator == 'lt' or operator == '<':
                        conditions.append(column < operand)
                    elif operator == 'lte' or operator == '<=':
                        conditions.append(column <= operand)
                    elif operator == 'in':
                        conditions.append(column.in_(operand))
                    elif operator == 'not_in' or operator == 'notIn':
                        conditions.append(~column.in_(operand))
                    elif operator == 'like':
                        conditions.append(column.like(operand))
                    elif operator == 'ilike':
                        conditions.append(column.ilike(operand))
                    elif operator == 'is_null' or operator == 'isNull':
                        conditions.append(column.is_(None) if operand else column.isnot(None))
            # Handle direct value comparison
            else:
                conditions.append(column == value)
        
        return conditions

    def _apply_relations(self, stmt, relations: List[str]):
        """
        Apply eager loading for relations.
        Supports deep relations like 'user.profile.address'
        """
        for relation in relations:
            if '.' in relation:
                # Deep relation: 'profile.address'
                parts = relation.split('.')
                current_model = self.model
                load_option = None
                
                for i, part in enumerate(parts):
                    if not hasattr(current_model, part):
                        break
                    
                    if i == 0:
                        load_option = selectinload(getattr(current_model, part))
                    else:
                        load_option = load_option.selectinload(getattr(current_model, part))
                    
                    # Get the related model for next iteration
                    relation_attr = getattr(current_model, part)
                    if hasattr(relation_attr.property, 'mapper'):
                        current_model = relation_attr.property.mapper.class_
                
                if load_option:
                    stmt = stmt.options(load_option)
            else:
                # Simple relation
                if hasattr(self.model, relation):
                    stmt = stmt.options(selectinload(getattr(self.model, relation)))
        
        return stmt

    def _apply_ordering(self, stmt, options: Dict):
        """Apply ORDER BY clause"""
        if options.get('order'):
            for field, direction in options['order'].items():
                if hasattr(self.model, field):
                    column = getattr(self.model, field)
                    stmt = stmt.order_by(
                        column.desc() if direction.upper() == 'DESC' else column.asc()
                    )
        return stmt

    def _apply_pagination(self, stmt, options: Dict):
        """Apply LIMIT and OFFSET"""
        if options.get('skip'):
            stmt = stmt.offset(options['skip'])
        if options.get('take'):
            stmt = stmt.limit(options['take'])
        return stmt

    def _get_nested_value(self, entity, field_path: str):
        """
        Get nested field value from entity.
        Example: 'profile.address.city' -> entity.profile.address.city
        """
        parts = field_path.split('.')
        value = entity
        
        for part in parts:
            if value is None:
                return None
            if hasattr(value, part):
                value = getattr(value, part)
            else:
                return None
        
        return value
