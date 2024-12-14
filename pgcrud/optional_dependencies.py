
__all__ = [
    'is_pydantic_installed',
]


try:
    import pydantic
    is_pydantic_installed = True
except ImportError:
    is_pydantic_installed = False
