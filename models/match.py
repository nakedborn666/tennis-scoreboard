from models.base import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import ForeignKey, CHAR, Text


class MatchModel(Base):
    __tablename__ = "matches"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    uuid: Mapped[str] = mapped_column(CHAR(36), unique=True, nullable=False)
    player1_id: Mapped[int] = mapped_column(ForeignKey("players.id"))
    player2_id: Mapped[int] = mapped_column(ForeignKey("players.id"))
    winner_id: Mapped[int | None] = mapped_column(ForeignKey("players.id"))
    score: Mapped[str] = mapped_column(Text, nullable=False)


    def __repr__(self):
        return f"MatchModel(id={self.id}, uuid={self.uuid}, winner_id={self.winner_id})"

