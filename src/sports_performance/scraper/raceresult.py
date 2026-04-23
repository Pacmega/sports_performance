"""Scraper for my.raceresult.com race results."""

import re
from datetime import date
from urllib.parse import parse_qs, urlparse

import httpx

from sports_performance.models.race import Discipline, Race, RaceResult, RaceResultSet

RESULTS_LIST_URL = "https://my2.raceresult.com/{race_id}/results/list"
RESULTS_LIMIT = 10000  # fetch all results in one request


class ScraperError(Exception):
    pass


def parse_raceresult_url(url: str) -> tuple[str, str, str | None]:
    """Extract (race_id, contest_num, key) from a my.raceresult.com URL.

    Accepts either:
    - Browser URL: https://my.raceresult.com/{id}/results#{contest_num}_{hash}
    - API URL: https://my2.raceresult.com/{id}/results/list?key={key}&contest={num}

    Returns (race_id, contest_num, key) where key is None for browser URLs
    (key will be auto-discovered when fetching results).

    Raises ValueError if the URL doesn't match either format.
    """
    parsed = urlparse(url)
    if parsed.netloc not in ("my.raceresult.com", "my2.raceresult.com"):
        raise ValueError(
            f"Expected my.raceresult.com or my2.raceresult.com, got: {parsed.netloc!r}"
        )
    path_parts = [p for p in parsed.path.split("/") if p]
    if not path_parts:
        raise ValueError("URL is missing a race ID in the path")
    race_id = path_parts[0]

    query_params = parse_qs(parsed.query)
    if query_params.get("key"):
        # Full API URL — key is present directly
        key = query_params["key"][0]
        contest_num = (query_params.get("contest") or ["1"])[0]
        return race_id, contest_num, key

    # Browser URL format: fragment is like "1_DDA59F"
    if not parsed.fragment:
        raise ValueError(
            "URL is missing a contest fragment (e.g. #1_DDA59F) or a key= query parameter"
        )
    contest_num = parsed.fragment.split("_")[0]
    if not contest_num.isdigit():
        raise ValueError(f"Could not parse contest number from fragment: {parsed.fragment!r}")
    return race_id, contest_num, None


def _discover_list_key(race_id: str, client: httpx.Client) -> str:
    """Fetch the result list key from the race's public API."""
    url = f"https://my.raceresult.com/{race_id}/resultlists"
    try:
        response = client.get(url, headers={"Accept": "application/json"})
        response.raise_for_status()
        data = response.json()
        for item in data:
            name = item.get("name") or item.get("ListName", "")
            if "Live" in name or "Leaderboard" in name:
                key = item.get("key") or item.get("Key")
                if key:
                    return key
        if data:
            key = data[0].get("key") or data[0].get("Key")
            if key:
                return key
    except (httpx.HTTPStatusError, httpx.NetworkError, KeyError, TypeError, ValueError):
        pass
    raise ScraperError(
        f"Could not auto-discover the API key for race {race_id}. "
        "Paste the full results/list URL from browser DevTools instead of the browser URL."
    )


def _parse_ordinal(rank_str: str) -> int | None:
    """Convert "1st", "2nd", "3rd"... to an integer, or None if unparseable."""
    match = re.match(r"^(\d+)", str(rank_str))
    return int(match.group(1)) if match else None


def _parse_race_date(list_info: dict) -> date | None:
    """Return the best available race date from list metadata.

    Priority:
    1. EventDate field (explicit race date, ISO format)
    2. Year from LastChange → date(year, 1, 1) as an approximate fallback
    3. None if neither is available
    """
    explicit = list_info.get("EventDate")
    if explicit:
        try:
            return date.fromisoformat(explicit)
        except ValueError:
            pass
    last_change = list_info.get("LastChange", "")
    try:
        year = int(last_change.split("-")[0])
        return date(year, 1, 1)
    except (AttributeError, ValueError, IndexError):
        return None


def _parse_distance(dist_str: str) -> float:
    """Convert "53 km" to 53.0."""
    match = re.match(r"^([\d.]+)", str(dist_str).strip())
    return float(match.group(1)) if match else 0.0


def _parse_api_response(raw: dict, race_id: str, contest_num: str) -> RaceResultSet:
    """Parse the my.raceresult.com results/list JSON into a RaceResultSet.

    Response shape:
      list.HeadLine2  → race name
      DataFields      → column labels (BIB, ID, OverallRank.th, FLNAME, ..., Finish, distance)
      data["#N_..."]  → list of arrays; last entry [total_count] is a sentinel
    """
    try:
        list_info = raw.get("list", {})
        race_name = list_info.get("HeadLine2") or list_info.get("HeadLine1") or f"Race {race_id}"

        data = raw.get("data", {})
        contest_prefix = f"#{contest_num}_"
        contest_key = next(
            (k for k in data if k.startswith(contest_prefix)),
            next(iter(data), None),
        )
        if contest_key is None:
            raise ScraperError(f"No result data found in API response for contest {contest_num}")

        data_fields = raw.get("DataFields", [])
        # Locate the column indices we care about
        idx_rank = data_fields.index("OverallRank.th") if "OverallRank.th" in data_fields else 2
        idx_name = data_fields.index("FLNAME") if "FLNAME" in data_fields else 3
        idx_time = data_fields.index("Finish") if "Finish" in data_fields else 6
        n_cols = len(data_fields)

        rows = data[contest_key]

        # Derive distance from first full-width row
        distance_km = 0.0
        for row in rows:
            if len(row) == n_cols:
                distance_km = _parse_distance(str(row[-1]))
                break

        race = Race(
            race_name=race_name,
            race_date=_parse_race_date(list_info),
            race_distance_km=distance_km,
            race_elevation_gain_m=None,
            race_discipline=Discipline.TRAIL_RUNNING,
        )

        results = []
        for row in rows:
            if len(row) != n_cols:  # skip sentinel entries like [151]
                continue
            results.append(
                RaceResult(
                    position=_parse_ordinal(row[idx_rank]),
                    athlete_name=str(row[idx_name]),
                    finish_time=str(row[idx_time]) if row[idx_time] else None,
                )
            )

        return RaceResultSet(race=race, results=results)

    except ScraperError:
        raise
    except (AttributeError, KeyError, TypeError, ValueError) as exc:
        raise ScraperError(f"Unexpected API response structure: {exc}") from exc


def fetch_results(
    race_id: str,
    contest_num: str,
    key: str | None = None,
    client: httpx.Client | None = None,
) -> RaceResultSet:
    """Fetch and parse results from the my.raceresult.com API.

    key: if None, will be auto-discovered (requires an extra HTTP call).
    client: optional pre-built httpx.Client for testing.
    Raises ScraperError on network failure or unexpected response.
    """
    own_client = client is None
    if own_client:
        client = httpx.Client(headers={"Accept": "application/json"})
    try:
        if key is None:
            key = _discover_list_key(race_id, client)
        url = RESULTS_LIST_URL.format(race_id=race_id)
        try:
            response = client.get(
                url,
                params={
                    "key": key,
                    "listname": "Online|Live Leaderboard",
                    "page": "results",
                    "contest": contest_num,
                    "r": "leaders",
                    "l": str(RESULTS_LIMIT),
                    "openedGroups": "{}",
                    "term": "",
                },
            )
            response.raise_for_status()
        except httpx.HTTPStatusError as exc:
            raise ScraperError(f"HTTP {exc.response.status_code} from {url}") from exc
        except httpx.NetworkError as exc:
            raise ScraperError(f"Network error: {exc}") from exc
        try:
            raw = response.json()
        except Exception as exc:
            raise ScraperError(f"Response is not valid JSON: {exc}") from exc
        return _parse_api_response(raw, race_id, contest_num)
    finally:
        if own_client:
            client.close()
