# Modules
from .products import ProductsModel
from db.postgres_db import Base, engine

Base.metadata.create_all(engine)
