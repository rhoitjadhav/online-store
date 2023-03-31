# Packages
from pydantic import BaseModel


class ProductsAddSchema(BaseModel):
    name: str
    description: str
    color: str
    size: str
    image: str
    price: int


class ProductsUpdateSchema(BaseModel):
    name: str
    description: str
    color: str
    size: str
    image: str
    price: int
