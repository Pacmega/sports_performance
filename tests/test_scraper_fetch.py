"""Tests for fetch_results using a mock httpx.Client."""

from datetime import date
from unittest.mock import MagicMock, patch

import httpx
import pytest

from sports_performance.models.race import Discipline, Race, RaceResult, RaceResultSet
from sports_performance.scraper.raceresult import ScraperError, fetch_results

TEST_KEY = "693425704ccbfc943d58148ba0fd527d"


def _make_mock_client(status_code=200, json_data=None, raise_exc=None):
    mock_response = MagicMock()
    mock_response.status_code = status_code
    mock_response.json.return_value = json_data or {}
    if status_code >= 400:
        mock_response.raise_for_status.side_effect = httpx.HTTPStatusError(
            "error", request=MagicMock(), response=mock_response
        )
    else:
        mock_response.raise_for_status.return_value = None

    mock_client = MagicMock()
    if raise_exc:
        mock_client.get.side_effect = raise_exc
    else:
        mock_client.get.return_value = mock_response
    return mock_client


def _make_sample_result_set():
    return RaceResultSet(
        race=Race(
            race_name="Test Race",
            race_date=date(2025, 4, 27),
            race_distance_km=50.0,
            race_elevation_gain_m=600.0,
            race_discipline=Discipline.TRAIL_RUNNING,
        ),
        results=[RaceResult(position=1, athlete_name="Alice", finish_time="04:12:33")],
    )


def test_fetch_results_calls_correct_url():
    mock_client = _make_mock_client(json_data={})
    with patch(
        "sports_performance.scraper.raceresult._parse_api_response",
        return_value=_make_sample_result_set(),
    ):
        fetch_results("370985", "1", key=TEST_KEY, client=mock_client)
    call_args = mock_client.get.call_args
    url = call_args[0][0]
    assert "370985" in url
    params = call_args[1].get("params", {})
    assert params.get("key") == TEST_KEY
    assert params.get("contest") == "1"


def test_fetch_results_returns_race_result_set():
    mock_client = _make_mock_client(json_data={})
    expected = _make_sample_result_set()
    with patch(
        "sports_performance.scraper.raceresult._parse_api_response",
        return_value=expected,
    ):
        result = fetch_results("370985", "1", key=TEST_KEY, client=mock_client)
    assert result is expected


def test_fetch_results_raises_scraper_error_on_http_404():
    mock_client = _make_mock_client(status_code=404)
    with pytest.raises(ScraperError, match="HTTP 404"):
        fetch_results("370985", "1", key=TEST_KEY, client=mock_client)


def test_fetch_results_raises_scraper_error_on_network_error():
    mock_client = _make_mock_client(raise_exc=httpx.NetworkError("connection refused"))
    with pytest.raises(ScraperError, match="Network error"):
        fetch_results("370985", "1", key=TEST_KEY, client=mock_client)
