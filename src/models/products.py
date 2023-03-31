# Packages
from sqlalchemy.orm import Mapped, mapped_column

# Modules
from db.postgres_db import Base


class ProductsModel(Base):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column()
    description: Mapped[str] = mapped_column()
    color: Mapped[str] = mapped_column()
    size: Mapped[str] = mapped_column()
    image: Mapped[str] = mapped_column()
    price: Mapped[int] = mapped_column()
