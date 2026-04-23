"""Sports performance analysis CLI."""

import typer
import questionary

app = typer.Typer(help="Sports performance analysis CLI.")

MAIN_OPTIONS = ["Scrape", "Analyze", "Quit"]
SCRAPE_OPTIONS = [
    "Collect race results",
    "List stored races",
    "Delete stored race data",
    "Back",
    "Quit",
]
ANALYZE_OPTIONS = ["Percentile ranking", "Target finishing time", "Back", "Quit"]


def _default_scrape_ask(choices):
    return questionary.select("Scrape:", choices=choices).ask()


def show_scrape_menu(ask_fn=None) -> None:
    if ask_fn is None:
        ask_fn = _default_scrape_ask
    while True:
        choice = ask_fn(SCRAPE_OPTIONS)
        if choice == "Collect race results":
            typer.echo("[TODO] scrape collect: not yet implemented.")
        elif choice == "List stored races":
            typer.echo("[TODO] scrape list: not yet implemented.")
        elif choice == "Delete stored race data":
            typer.echo("[TODO] scrape delete: not yet implemented.")
        elif choice == "Back":
            return
        elif choice == "Quit" or choice is None:
            raise SystemExit(0)


def _default_analyze_ask(choices):
    return questionary.select("Analyze:", choices=choices).ask()


def show_analyze_menu(ask_fn=None) -> None:
    if ask_fn is None:
        ask_fn = _default_analyze_ask
    while True:
        choice = ask_fn(ANALYZE_OPTIONS)
        if choice == "Percentile ranking":
            typer.echo("[TODO] analyze percentile: not yet implemented.")
        elif choice == "Target finishing time":
            typer.echo("[TODO] analyze target-time: not yet implemented.")
        elif choice == "Back":
            return
        elif choice == "Quit" or choice is None:
            raise SystemExit(0)


def _default_main_ask(choices):
    return questionary.select("Sports Performance:", choices=choices).ask()


def show_main_menu(ask_fn=None, scrape_menu_fn=None, analyze_menu_fn=None) -> None:
    if ask_fn is None:
        ask_fn = _default_main_ask
    if scrape_menu_fn is None:
        scrape_menu_fn = show_scrape_menu
    if analyze_menu_fn is None:
        analyze_menu_fn = show_analyze_menu
    while True:
        choice = ask_fn(MAIN_OPTIONS)
        if choice == "Scrape":
            scrape_menu_fn()
        elif choice == "Analyze":
            analyze_menu_fn()
        elif choice == "Quit" or choice is None:
            raise SystemExit(0)


@app.callback(invoke_without_command=True)
def main(ctx: typer.Context) -> None:
    """Sports performance analysis CLI."""
    if ctx.invoked_subcommand is None:
        show_main_menu()


def entrypoint() -> None:
    app()
