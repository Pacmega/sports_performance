"""Tests for domain models."""

from datetime import date

import pytest
from pydantic import ValidationError

from sports_performance.models.race import Discipline, Race, RaceResult, RaceResultSet


def _sample_race():
    return Race(
        race_name="Test Race",
        race_date=date(2025, 4, 27),
        race_distance_km=50.0,
        race_elevation_gain_m=2500.0,
        race_discipline=Discipline.TRAIL_RUNNING,
    )


def test_race_valid_construction():
    race = _sample_race()
    assert race.race_name == "Test Race"
    assert race.race_date == date(2025, 4, 27)
    assert race.race_distance_km == 50.0
    assert race.race_elevation_gain_m == 2500.0
    assert race.race_discipline == Discipline.TRAIL_RUNNING


def test_race_requires_name_distance_and_discipline():
    with pytest.raises(ValidationError):
        Race(race_name="Incomplete")


def test_race_date_is_optional():
    race = Race(
        race_name="No Date Race",
        race_distance_km=50.0,
        race_discipline=Discipline.TRAIL_RUNNING,
    )
    assert race.race_date is None


def test_race_elevation_is_optional():
    race = Race(
        race_name="No Elevation Race",
        race_distance_km=50.0,
        race_discipline=Discipline.TRAIL_RUNNING,
    )
    assert race.race_elevation_gain_m is None


def test_result_defaults_dnf_dns_false():
    result = RaceResult(position=1, athlete_name="Alice", finish_time="02:34:17")
    assert result.dnf is False
    assert result.dns is False


def test_result_dnf_clears_position_and_time_by_convention():
    result = RaceResult(athlete_name="Bob", dnf=True)
    assert result.position is None
    assert result.finish_time is None
    assert result.dnf is True


def test_result_dns():
    result = RaceResult(athlete_name="Carol", dns=True)
    assert result.position is None
    assert result.finish_time is None
    assert result.dns is True


def test_race_result_set_empty_results_allowed():
    rs = RaceResultSet(race=_sample_race(), results=[])
    assert rs.results == []


def test_race_result_set_with_results():
    results = [
        RaceResult(position=1, athlete_name="Alice", finish_time="02:34:17"),
        RaceResult(position=2, athlete_name="Bob", finish_time="02:40:00"),
    ]
    rs = RaceResultSet(race=_sample_race(), results=results)
    assert len(rs.results) == 2


def test_discipline_enum_values():
    assert Discipline.TRAIL_RUNNING.value == "trail_running"
    assert Discipline.ROAD_RUNNING.value == "road_running"
