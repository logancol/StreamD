from __future__ import annotations
from sqlalchemy import BigInteger, Date, ForeignKeyConstraint, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column
from app.db.sa_base import Base

class Game(Base):
    __tablename__ = "game"
    __table_args__ = (
        ForeignKeyConstraint(
            ["home_team_id", "home_team_abrev"],
            ["modern_team_index.id", "modern_team_index.abrev"],
        ),
        ForeignKeyConstraint(
            ["away_team_id", "away_team_abrev"],
            ["modern_team_index.id", "modern_team_index.abrev"],
        ),
    )
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    season_id: Mapped[int | None] = mapped_column(Integer, nullable=True)
    home_team_id: Mapped[int | None] = mapped_column(BigInteger, nullable=True)
    home_team_abrev: Mapped[str | None] = mapped_column(String(3), nullable=True)
    away_team_id: Mapped[int | None] = mapped_column(BigInteger, nullable=True)
    away_team_abrev: Mapped[str | None] = mapped_column(String(3), nullable=True)
    date: Mapped[object | None] = mapped_column(Date, nullable=True)
    season_type: Mapped[str | None] = mapped_column(Text, nullable=True)
    winner_id: Mapped[int | None] = mapped_column(BigInteger, nullable=True)