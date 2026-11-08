from models.base import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String



class PlayerModel(Base):
    __tablename__ = "players"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)


