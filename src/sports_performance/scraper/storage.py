"""CSV serialisation and file storage for race results."""

import csv
from pathlib import Path

from sports_performance.models.race import RaceResultSet

CSV_COLUMNS = [
    "position",
    "athlete_name",
    "finish_time",
    "dnf",
    "dns",
    "race_name",
    "race_date",
    "race_distance_km",
    "race_elevation_gain_m",
    "race_discipline",
]


def results_to_csv_rows(result_set: RaceResultSet) -> list[dict]:
    race = result_set.race
    rows = []
    for r in result_set.results:
        rows.append(
            {
                "position": r.position if r.position is not None else "",
                "athlete_name": r.athlete_name,
                "finish_time": r.finish_time if r.finish_time is not None else "",
                "dnf": r.dnf,
                "dns": r.dns,
                "race_name": race.race_name,
                "race_date": race.race_date.isoformat() if race.race_date else "",
                "race_distance_km": race.race_distance_km,
                "race_elevation_gain_m": race.race_elevation_gain_m
                if race.race_elevation_gain_m is not None
                else "",
                "race_discipline": race.race_discipline.value,
            }
        )
    return rows


def derive_csv_filename(result_set: RaceResultSet) -> str:
    slug = result_set.race.race_name.lower().replace(" ", "_")
    date_str = (
        result_set.race.race_date.isoformat() if result_set.race.race_date else "unknown_date"
    )
    return f"{slug}_{date_str}.csv"


def save_results(result_set: RaceResultSet, output_dir: Path) -> Path:
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    path = output_dir / derive_csv_filename(result_set)
    rows = results_to_csv_rows(result_set)
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=CSV_COLUMNS, extrasaction="raise")
        writer.writeheader()
        writer.writerows(rows)
    return path.resolve()
