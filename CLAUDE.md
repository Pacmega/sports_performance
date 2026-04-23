# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

```bash
# Install / sync dependencies
uv sync

# Add a runtime dependency
uv add <package>

# Add a dev dependency
uv add --dev <package>

# Lint
ruff check .

# Format
ruff format .

# Run all tests
uv run pytest

# Run a single test file or test
uv run pytest tests/test_cli.py
uv run pytest tests/test_cli.py::test_function_name

# Run the CLI
uv run sports-perf
```

## Architecture

This is an early-stage Python CLI tool for scraping race results and computing performance statistics. The project is in Phase 1 (CLI only); a web GUI is planned for Phase 2.

### Package layout

```
src/sports_performance/
├── cli.py          # CLI entrypoint (`sports-perf` command via pyproject.toml)
├── scraper/        # Race result scraping (stub)
└── analytics/      # Performance calculations (stub)
```

### Domain model (see DATA_MODEL.md for full spec)

Three core entities:

- **Race** — event metadata (name, date, discipline, distance, elevation gain)
- **Athlete** — identified by name only for MVP
- **RaceResult** — links athlete to race; carries position, finish time, DNF/DNS flag

Data is stored as CSV files (one per race), not a database.

### Non-functional constraints (from SPEC.md)

- Keep core logic decoupled from I/O (scraping, file writing) so business logic stays unit-testable
- Design for extensibility to new sports/disciplines and new data sources
- MVP explicitly excludes: user authentication, categorised data storage, real-time updates, mobile support

### Key design decisions

- **Sources to scrape**: `itra.run` and `my.raceresult.com` are the priority targets; `utmb.world` and direct race sites are secondary. Example HTML fixtures are in `example_data/`.
- **Performance metric**: primary output is percentile rank (`position / total_finishers * 100`); age grading and equivalent-time formulas are deferred.
- **No auth in MVP**: scraping is unauthenticated; rate limiting and user-agent headers are expected but not yet implemented.
- **Tech stack not yet locked**: `httpx`, `pydantic`, and `polars` are the suggested choices (see TODO.md), but none are installed yet — add with `uv add` when building the scraper.

### What still needs to be built

See `TODO.md` for the current gap analysis. The most critical open decisions are:
1. Pick a single data source and race URL to target first.
2. Install scraper libraries (`httpx`, `pydantic`, `polars`).
3. Create Pydantic models in `src/sports_performance/models/` derived from DATA_MODEL.md.
4. Implement CLI commands in `cli.py`.
