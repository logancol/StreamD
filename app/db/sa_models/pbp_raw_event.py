from __future__ import annotations
from sqlalchemy import BigInteger, Boolean, Float, ForeignKey, ForeignKeyConstraint, Integer, PrimaryKeyConstraint, String, Text, text
from sqlalchemy.dialects.postgresql import INTERVAL, TIMESTAMP
from sqlalchemy.orm import Mapped, mapped_column
from app.db.sa_base import Base

class PbpRawEvent(Base):
    __tablename__ = "pbp_raw_event"
    __table_args__ = (
        PrimaryKeyConstraint("game_id", "event_num"),
        ForeignKeyConstraint(
            ["home_team_id", "home_team_abrev"],
            ["modern_team_index.id", "modern_team_index.abrev"],
        ),
        ForeignKeyConstraint(
            ["away_team_id", "away_team_abrev"],
            ["modern_team_index.id", "modern_team_index.abrev"],
        ),
        ForeignKeyConstraint(
            ["possession_team_id", "possession_team_abrev"],
            ["modern_team_index.id", "modern_team_index.abrev"],
        ),
        ForeignKeyConstraint(
            ["event_team_id", "event_team_abrev"],
            ["modern_team_index.id", "modern_team_index.abrev"],
        ),
    )
    game_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("game.id"), nullable=False)
    season_id: Mapped[int | None] = mapped_column(Integer, nullable=True)
    season_type: Mapped[str | None] = mapped_column(Text, nullable=True)
    event_num: Mapped[int] = mapped_column(Integer, nullable=False)
    event_type: Mapped[str] = mapped_column(Text, nullable=False)
    event_subtype: Mapped[str | None] = mapped_column(Text, nullable=True)
    home_score: Mapped[int | None] = mapped_column(Integer, nullable=True)
    away_score: Mapped[int | None] = mapped_column(Integer, nullable=True)
    period: Mapped[int] = mapped_column(Integer, nullable=False)
    clock: Mapped[object | None] = mapped_column(INTERVAL, nullable=True)
    home_team_id: Mapped[int | None] = mapped_column(BigInteger, nullable=True)
    away_team_id: Mapped[int | None] = mapped_column(BigInteger, nullable=True)
    home_team_abrev: Mapped[str | None] = mapped_column(String(3), nullable=True)
    away_team_abrev: Mapped[str | None] = mapped_column(String(3), nullable=True)
    possession_team_id: Mapped[int | None] = mapped_column(BigInteger, nullable=True)
    possession_team_abrev: Mapped[str | None] = mapped_column(String(3), nullable=True)
    event_team_id: Mapped[int | None] = mapped_column(BigInteger, nullable=True)
    event_team_abrev: Mapped[str | None] = mapped_column(String(3), nullable=True)
    is_overtime: Mapped[bool | None] = mapped_column(Boolean, nullable=True)
    shooter_id: Mapped[int | None] = mapped_column(BigInteger, ForeignKey("player.id"), nullable=True)
    assister_id: Mapped[int | None] = mapped_column(BigInteger, ForeignKey("player.id"), nullable=True)
    jump_ball_winner_id: Mapped[int | None] = mapped_column(BigInteger, ForeignKey("player.id"), nullable=True)
    jump_ball_loser_id: Mapped[int | None] = mapped_column(BigInteger, ForeignKey("player.id"), nullable=True)
    jump_ball_recovered_id: Mapped[int | None] = mapped_column(BigInteger, ForeignKey("player.id"), nullable=True)
    rebounder_id: Mapped[int | None] = mapped_column(BigInteger, ForeignKey("player.id"), nullable=True)
    turnover_id: Mapped[int | None] = mapped_column(BigInteger, ForeignKey("player.id"), nullable=True)
    foul_drawn_id: Mapped[int | None] = mapped_column(BigInteger, ForeignKey("player.id"), nullable=True)
    fouler_id: Mapped[int | None] = mapped_column(BigInteger, ForeignKey("player.id"), nullable=True)
    stealer_id: Mapped[int | None] = mapped_column(BigInteger, ForeignKey("player.id"), nullable=True)
    blocker_id: Mapped[int | None] = mapped_column(BigInteger, ForeignKey("player.id"), nullable=True)
    sub_in_id: Mapped[int | None] = mapped_column(BigInteger, ForeignKey("player.id"), nullable=True)
    sub_out_id: Mapped[int | None] = mapped_column(BigInteger, ForeignKey("player.id"), nullable=True)
    foul_is_technical: Mapped[bool | None] = mapped_column(Boolean, nullable=True)
    foul_is_personal: Mapped[bool | None] = mapped_column(Boolean, nullable=True)
    foul_is_offensive: Mapped[bool | None] = mapped_column(Boolean, nullable=True)
    team_turnover: Mapped[bool | None] = mapped_column(Boolean, nullable=True)
    team_rebound: Mapped[bool | None] = mapped_column(Boolean, nullable=True)
    offensive_rebound: Mapped[bool | None] = mapped_column(Boolean, nullable=True)
    side: Mapped[str | None] = mapped_column(Text, nullable=True)
    descriptor: Mapped[str | None] = mapped_column(Text, nullable=True)
    area: Mapped[str | None] = mapped_column(Text, nullable=True)
    area_detail: Mapped[str | None] = mapped_column(Text, nullable=True)
    shot_distance: Mapped[float | None] = mapped_column(Float, nullable=True)
    shot_made: Mapped[bool | None] = mapped_column(Boolean, nullable=True)
    shot_value: Mapped[int | None] = mapped_column(Integer, nullable=True)
    shot_x: Mapped[float | None] = mapped_column(Float, nullable=True)
    shot_y: Mapped[float | None] = mapped_column(Float, nullable=True)
    created_at: Mapped[object] = mapped_column(TIMESTAMP(timezone=False), server_default=text("now()"), nullable=True)