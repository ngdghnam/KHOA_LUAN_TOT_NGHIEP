from sqlalchemy.inspection import inspect
from collections.abc import Iterable

def serialize(obj):
    if obj is None:
        return None

    if isinstance(obj, list):
        return [serialize(item) for item in obj]

    if hasattr(obj, "__table__"):
        return {
            c.key: getattr(obj, c.key)
            for c in inspect(obj).mapper.column_attrs
        }

    return obj
