# AGENTS.md

## Setup

- **Package manager**: uv (not pip/poetry)
- **Run commands**: `uv sync`, `uv run <script>`, `uv pip install <package>`
- **Add dependencies**: `uv add <package>` or `uv add --dev <package>`

## Development

- **Linting/Formatting**: ruff (`ruff check .`, `ruff format .`)
- **Run tests**: `uv run pytest` (or `uv run python -m pytest`)

## Project Structure (evolving)

- Start with CLI entrypoint, add web GUI later
- Core features: race result scraping, expected finishing time calculations

## Notes

- This is a new project - expand AGENTS.md as conventions are established
