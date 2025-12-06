from typing import TypeVar, Generic, List, Optional, Tuple, Any, Dict, TypedDict

class Options(TypedDict, total=False):
    where: Optional[Dict[str, Any]]
    relations: Optional[List[str]]
    select: Optional[List[str]]

class FindOptions(TypedDict, total=False):
    where: Optional[Dict[str, Any]]
    relations: Optional[List[str]]
    select: Optional[List[str]]
    skip: Optional[int]
    take: Optional[int]
    order: Optional[Dict[str, str]]