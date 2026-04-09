# Sports Performance Analysis

CLI tool for scraping race results and calculating expected finishing times.

## Setup

```bash
uv sync
```

## Development

```bash
# Lint
ruff check .

# Format
ruff format .

# Test
uv run pytest
```

## Project Structure

```
src/sports_performance/
├── cli.py          # CLI entrypoint
├── scraper/        # Race result scraping
└── analytics/     # Performance calculations
```

## Documentation

- [SPEC.md](SPEC.md) - Project specification
- [DATA_MODEL.md](DATA_MODEL.md) - Data model template (fill in)