"""Domain models for race results."""

from datetime import date
from enum import Enum

from pydantic import BaseModel


class Discipline(str, Enum):
    TRAIL_RUNNING = "trail_running"
    ROAD_RUNNING = "road_running"


class Race(BaseModel):
    race_name: str
    race_date: date | None = None
    race_distance_km: float
    race_elevation_gain_m: float | None = None
    race_discipline: Discipline


class RaceResult(BaseModel):
    position: int | None = None
    athlete_name: str
    finish_time: str | None = None
    dnf: bool = False
    dns: bool = False


class RaceResultSet(BaseModel):
    race: Race
    results: list[RaceResult]
