import importlib.util


__all__ = [
    'is_pydantic_installed',
]


is_pydantic_installed =  bool(importlib.util.find_spec('pydantic'))
