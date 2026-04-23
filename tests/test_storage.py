"""Tests for CSV storage."""

import csv
from datetime import date

from sports_performance.models.race import Discipline, Race, RaceResult, RaceResultSet
from sports_performance.scraper.storage import (
    CSV_COLUMNS,
    derive_csv_filename,
    results_to_csv_rows,
    save_results,
)


def _sample_result_set():
    race = Race(
        race_name="Utrechtse Heuvelrug Ultra Trail 50K",
        race_date=date(2025, 4, 27),
        race_distance_km=50.0,
        race_elevation_gain_m=600.0,
        race_discipline=Discipline.TRAIL_RUNNING,
    )
    results = [
        RaceResult(position=1, athlete_name="Alice", finish_time="04:12:33"),
        RaceResult(athlete_name="Bob", dnf=True),
        RaceResult(athlete_name="Carol", dns=True),
    ]
    return RaceResultSet(race=race, results=results)


def test_results_to_csv_rows_column_order():
    rs = _sample_result_set()
    rows = results_to_csv_rows(rs)
    assert list(rows[0].keys()) == CSV_COLUMNS


def test_results_to_csv_rows_dnf_athlete_has_empty_finish_time():
    rs = _sample_result_set()
    rows = results_to_csv_rows(rs)
    dnf_row = rows[1]
    assert dnf_row["finish_time"] == ""
    assert dnf_row["position"] == ""
    assert dnf_row["dnf"] is True


def test_results_to_csv_rows_dns_athlete_has_empty_position():
    rs = _sample_result_set()
    rows = results_to_csv_rows(rs)
    dns_row = rows[2]
    assert dns_row["position"] == ""
    assert dns_row["dns"] is True


def test_results_to_csv_rows_includes_race_metadata():
    rs = _sample_result_set()
    rows = results_to_csv_rows(rs)
    row = rows[0]
    assert row["race_name"] == "Utrechtse Heuvelrug Ultra Trail 50K"
    assert row["race_date"] == "2025-04-27"
    assert row["race_distance_km"] == 50.0
    assert row["race_elevation_gain_m"] == 600.0
    assert row["race_discipline"] == "trail_running"


def test_derive_csv_filename_with_full_date():
    rs = _sample_result_set()
    assert derive_csv_filename(rs) == "utrechtse_heuvelrug_ultra_trail_50k_2025-04-27.csv"


def test_derive_csv_filename_with_year_fallback():
    race = Race(
        race_name="50km Rhenen",
        race_date=date(2025, 1, 1),
        race_distance_km=53.0,
        race_discipline=Discipline.TRAIL_RUNNING,
    )
    rs = RaceResultSet(race=race, results=[])
    assert derive_csv_filename(rs) == "50km_rhenen_2025-01-01.csv"


def test_derive_csv_filename_no_date():
    race = Race(
        race_name="No Date Race",
        race_distance_km=50.0,
        race_discipline=Discipline.TRAIL_RUNNING,
    )
    rs = RaceResultSet(race=race, results=[])
    assert derive_csv_filename(rs) == "no_date_race_unknown_date.csv"


def test_results_to_csv_rows_optional_fields_empty_string():
    race = Race(
        race_name="No Date Race",
        race_distance_km=50.0,
        race_discipline=Discipline.TRAIL_RUNNING,
    )
    rs = RaceResultSet(
        race=race,
        results=[RaceResult(position=1, athlete_name="Alice", finish_time="04:00:00")],
    )
    rows = results_to_csv_rows(rs)
    assert rows[0]["race_date"] == ""
    assert rows[0]["race_elevation_gain_m"] == ""


def test_save_results_creates_data_dir(tmp_path):
    output_dir = tmp_path / "data"
    assert not output_dir.exists()
    save_results(_sample_result_set(), output_dir)
    assert output_dir.exists()


def test_save_results_returns_correct_path(tmp_path):
    path = save_results(_sample_result_set(), tmp_path)
    assert path.name == "utrechtse_heuvelrug_ultra_trail_50k_2025-04-27.csv"
    assert path.exists()


def test_save_results_csv_content_is_correct(tmp_path):
    path = save_results(_sample_result_set(), tmp_path)
    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = list(reader)
    assert len(rows) == 3
    assert rows[0]["athlete_name"] == "Alice"
    assert rows[0]["position"] == "1"
    assert rows[0]["finish_time"] == "04:12:33"
    assert rows[1]["athlete_name"] == "Bob"
    assert rows[1]["dnf"] == "True"
    assert rows[2]["dns"] == "True"
