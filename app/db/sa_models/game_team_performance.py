from __future__ import annotations
from sqlalchemy import BigInteger, Boolean, Float, ForeignKey, ForeignKeyConstraint, Integer, PrimaryKeyConstraint, String
from sqlalchemy.orm import Mapped, mapped_column
from app.db.sa_base import Base

class GameTeamPerformance(Base):
    __tablename__ = "game_team_performance"
    __table_args__ = (
        PrimaryKeyConstraint("game_id", "team_id"),
        ForeignKeyConstraint(
            ["team_id", "team_abrev"],
            ["modern_team_index.id", "modern_team_index.abrev"],
        ),
    )
    game_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("game.id"), nullable=False)
    team_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
    team_abrev: Mapped[str | None] = mapped_column(String(3), nullable=True)
    mins: Mapped[int | None] = mapped_column(Integer, nullable=True)
    pts: Mapped[int | None] = mapped_column(Integer, nullable=True)
    overtime: Mapped[bool | None] = mapped_column(Boolean, nullable=True)
    field_goals_made: Mapped[int | None] = mapped_column(Integer, nullable=True)
    field_goals_attempted: Mapped[int | None] = mapped_column(Integer, nullable=True)
    field_goal_percentage: Mapped[float | None] = mapped_column(Float, nullable=True)
    three_pointers_made: Mapped[int | None] = mapped_column(Integer, nullable=True)
    three_pointers_attempted: Mapped[int | None] = mapped_column(Integer, nullable=True)
    three_pointer_percentage: Mapped[float | None] = mapped_column(Float, nullable=True)
    free_throws_made: Mapped[int | None] = mapped_column(Integer, nullable=True)
    free_throws_attempted: Mapped[int | None] = mapped_column(Integer, nullable=True)
    free_throw_percentage: Mapped[float | None] = mapped_column(Float, nullable=True)
    offensive_rebounds: Mapped[int | None] = mapped_column(Integer, nullable=True)
    defensive_rebounds: Mapped[int | None] = mapped_column(Integer, nullable=True)
    total_rebounds: Mapped[int | None] = mapped_column(Integer, nullable=True)
    assists: Mapped[int | None] = mapped_column(Integer, nullable=True)
    steals: Mapped[int | None] = mapped_column(Integer, nullable=True)
    blocks: Mapped[int | None] = mapped_column(Integer, nullable=True)
    turnovers: Mapped[int | None] = mapped_column(Integer, nullable=True)
    personal_fouls: Mapped[int | None] = mapped_column(Integer, nullable=True)
    plus_minus: Mapped[int | None] = mapped_column(Integer, nullable=True)