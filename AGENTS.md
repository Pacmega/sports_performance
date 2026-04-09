# AGENTS.md

## Setup

- **Package manager**: uv (not pip/poetry)
- **Sync environment**: `uv sync`
- **Add dependencies**: `uv add <package>` or `uv add --dev <package>`
- **Run scripts**: `uv run <script>`

## Development

- **Linting/Formatting**: ruff (`ruff check .`, `ruff format .`)
- **Run tests**: `uv run pytest` (or `uv run python -m pytest`)

## Project Structure (evolving)

- Start with CLI entrypoint, add web GUI later
- Core features: race result scraping, expected finishing time calculations

## Notes

- This is a new project - expand AGENTS.md as conventions are established
