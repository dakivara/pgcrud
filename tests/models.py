from pydantic import BaseModel


__all__ = ['Customer']


class Customer(BaseModel):
    id: int
    name: str
