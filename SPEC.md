# Project Specification

## Overview

A data science tool for sports performance analysis, starting with CLI and later expanding to web GUI.

## Core Features

### 1. Race Result Scraping
- Scrape race results from web sources
- Parse and normalize data from various formats
- Store data for race results in csv format per race
- Handle pagination, rate limiting, and error cases

### 2. Expected Finishing Time Calculations
- Calculate expected finishing times based on historical data
- Determine percentile rankings (e.g., "top 45-50-55% of finishers")
- Provide target times for desired performance levels

## Tech Stack

| Concern         | Library       | Notes                                                    |
| --------------- | ------------- | -------------------------------------------------------- |
| HTTP client     | `httpx`       | Sync and async; nearly identical API to `requests`       |
| HTML parsing    | `selectolax`  | CSS selectors; needed for UTMB and direct race sites     |
| Data validation | `pydantic`    | Typed models for Race, Athlete, RaceResult               |
| CLI framework   | `typer`       | Built on `click`; subcommands and `--help` for free      |
| Data analysis   | `polars`      | Deferred until cross-race aggregate analytics are needed |
| Packaging       | `uv` + `ruff` | Already in use                                           |
| Testing         | `pytest`      | Standard for unit testing                                |

**Initial data source**: `my.raceresult.com` — serves JSON via API, so no HTML parsing needed for the first scraper.

## Architecture

### CLI Entrypoint (Phase 1)
- Command-line interface for all core operations
- Focus on scriptability and automation

### Web GUI (Phase 2)
- Web-based interface for visualization and exploration
- Build on top of core library functionality

## Non-Functional Requirements

- Clean separation between core logic and I/O concerns
- Testable business logic
- Extensible for new sports/disciplines
- Configurable data sources

## Out of Scope (MVP)

- User authentication
- Data storage categorized in different categories
- Real-time updates
- Mobile support