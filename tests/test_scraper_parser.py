"""Tests for URL parsing and API response parsing."""

import json
from datetime import date
from pathlib import Path

import pytest

from sports_performance.scraper.raceresult import (
    ScraperError,
    _parse_api_response,
    parse_raceresult_url,
)

FIXTURE_PATH = Path(__file__).parent / "fixtures" / "raceresult_370985_response.json"

# Minimal raw dict shape used by several tests
_BASE_RAW = {
    "list": {"HeadLine2": "Test Race"},
    "data": {"#1_Test Race": []},
    "DataFields": [],
}


def test_parse_raceresult_url_browser_url():
    race_id, contest_num, key = parse_raceresult_url(
        "https://my.raceresult.com/370985/results#1_DDA59F"
    )
    assert race_id == "370985"
    assert contest_num == "1"
    assert key is None


def test_parse_raceresult_url_api_url():
    race_id, contest_num, key = parse_raceresult_url(
        "https://my2.raceresult.com/370985/results/list"
        "?key=693425704ccbfc943d58148ba0fd527d&contest=1&listname=Online%7CLive+Leaderboard"
    )
    assert race_id == "370985"
    assert contest_num == "1"
    assert key == "693425704ccbfc943d58148ba0fd527d"


def test_parse_raceresult_url_wrong_domain():
    with pytest.raises(ValueError, match="my.raceresult.com"):
        parse_raceresult_url("https://itra.run/370985/results#1_DDA59F")


def test_parse_raceresult_url_missing_fragment():
    with pytest.raises(ValueError, match="missing a contest fragment"):
        parse_raceresult_url("https://my.raceresult.com/370985/results")


def test_parse_raceresult_url_missing_race_id():
    with pytest.raises(ValueError, match="missing a race ID"):
        parse_raceresult_url("https://my.raceresult.com/#1_DDA59F")


# --- date parsing ---


def test_parse_api_response_explicit_date_used_when_present():
    """An explicit EventDate in the list metadata takes priority over LastChange."""
    raw = {
        "list": {
            "HeadLine2": "Test Race",
            "EventDate": "2024-06-15",
            "LastChange": "2025-10-23 13:50:19",
        },
        "data": {"#1_Test Race": []},
        "DataFields": [],
    }
    result_set = _parse_api_response(raw, "12345", "1")
    assert result_set.race.race_date == date(2024, 6, 15)


def test_parse_api_response_year_fallback_when_no_explicit_date():
    """Without an explicit date, the year from LastChange becomes Jan 1 of that year."""
    raw = json.loads(FIXTURE_PATH.read_text())
    result_set = _parse_api_response(raw, "370985", "1")
    assert result_set.race.race_date == date(2025, 1, 1)


def test_parse_api_response_no_date_at_all_is_none():
    """Without EventDate or LastChange, race_date is None."""
    raw = {**_BASE_RAW, "list": {"HeadLine2": "Test Race"}}
    result_set = _parse_api_response(raw, "12345", "1")
    assert result_set.race.race_date is None


# --- other response parsing ---


def test_parse_api_response_happy_path():
    raw = json.loads(FIXTURE_PATH.read_text())
    result_set = _parse_api_response(raw, "370985", "1")
    assert result_set.race.race_name == "50km Rhenen"
    assert len(result_set.results) == 151


def test_parse_api_response_first_finisher():
    raw = json.loads(FIXTURE_PATH.read_text())
    result_set = _parse_api_response(raw, "370985", "1")
    first = result_set.results[0]
    assert first.position == 1
    assert first.athlete_name == "Frits Gijsman"
    assert first.finish_time == "4:16:12"


def test_parse_api_response_distance_parsed():
    raw = json.loads(FIXTURE_PATH.read_text())
    result_set = _parse_api_response(raw, "370985", "1")
    assert result_set.race.race_distance_km == 53.0


def test_parse_api_response_sentinel_excluded():
    """The trailing [151] sentinel entry must not appear as a result."""
    raw = json.loads(FIXTURE_PATH.read_text())
    result_set = _parse_api_response(raw, "370985", "1")
    for r in result_set.results:
        assert r.athlete_name != ""


def test_parse_api_response_missing_key_raises_scraper_error():
    with pytest.raises(ScraperError):
        _parse_api_response(None, "370985", "1")
