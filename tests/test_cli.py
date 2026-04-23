"""Tests for CLI menu navigation."""

import pytest
from unittest.mock import patch
from sports_performance.cli import (
    show_main_menu,
    show_scrape_menu,
    show_analyze_menu,
    MAIN_OPTIONS,
    SCRAPE_OPTIONS,
    ANALYZE_OPTIONS,
)

# --- Option list tests ---


def test_main_options_contains_expected_entries():
    assert "Scrape" in MAIN_OPTIONS
    assert "Analyze" in MAIN_OPTIONS
    assert "Quit" in MAIN_OPTIONS


def test_scrape_options_contains_expected_entries():
    assert "Collect race results" in SCRAPE_OPTIONS
    assert "List stored races" in SCRAPE_OPTIONS
    assert "Delete stored race data" in SCRAPE_OPTIONS
    assert "Back" in SCRAPE_OPTIONS
    assert "Quit" in SCRAPE_OPTIONS


def test_analyze_options_contains_expected_entries():
    assert "Percentile ranking" in ANALYZE_OPTIONS
    assert "Target finishing time" in ANALYZE_OPTIONS
    assert "Back" in ANALYZE_OPTIONS
    assert "Quit" in ANALYZE_OPTIONS


# --- Main menu routing ---


def test_main_menu_quit_exits():
    choices = iter(["Quit"])
    with pytest.raises(SystemExit):
        show_main_menu(ask_fn=lambda _: next(choices))


def test_main_menu_routes_to_scrape_then_quits():
    # Scrape → Back → Quit
    main_calls = iter(["Scrape", "Quit"])

    with patch("sports_performance.cli.show_scrape_menu") as mock_scrape:
        mock_scrape.side_effect = lambda **_: None
        with pytest.raises(SystemExit):
            show_main_menu(
                ask_fn=lambda _: next(main_calls),
                scrape_menu_fn=mock_scrape,
            )
    mock_scrape.assert_called_once()


def test_main_menu_routes_to_analyze_then_quits():
    main_calls = iter(["Analyze", "Quit"])

    with patch("sports_performance.cli.show_analyze_menu") as mock_analyze:
        mock_analyze.side_effect = lambda **_: None
        with pytest.raises(SystemExit):
            show_main_menu(
                ask_fn=lambda _: next(main_calls),
                analyze_menu_fn=mock_analyze,
            )
    mock_analyze.assert_called_once()


# --- Scrape submenu ---


def test_scrape_collect_prints_todo(capsys):
    choices = iter(["Collect race results", "Back"])
    show_scrape_menu(ask_fn=lambda _: next(choices))
    captured = capsys.readouterr()
    assert "[TODO]" in captured.out
    assert "collect" in captured.out.lower()


def test_scrape_list_prints_todo(capsys):
    choices = iter(["List stored races", "Back"])
    show_scrape_menu(ask_fn=lambda _: next(choices))
    captured = capsys.readouterr()
    assert "[TODO]" in captured.out
    assert "list" in captured.out.lower()


def test_scrape_delete_prints_todo(capsys):
    choices = iter(["Delete stored race data", "Back"])
    show_scrape_menu(ask_fn=lambda _: next(choices))
    captured = capsys.readouterr()
    assert "[TODO]" in captured.out
    assert "delete" in captured.out.lower()


def test_scrape_back_returns_without_exit():
    choices = iter(["Back"])
    # Should return normally, not raise SystemExit
    show_scrape_menu(ask_fn=lambda _: next(choices))


def test_scrape_quit_exits():
    choices = iter(["Quit"])
    with pytest.raises(SystemExit):
        show_scrape_menu(ask_fn=lambda _: next(choices))


# --- Analyze submenu ---


def test_analyze_percentile_prints_todo(capsys):
    choices = iter(["Percentile ranking", "Back"])
    show_analyze_menu(ask_fn=lambda _: next(choices))
    captured = capsys.readouterr()
    assert "[TODO]" in captured.out
    assert "percentile" in captured.out.lower()


def test_analyze_target_time_prints_todo(capsys):
    choices = iter(["Target finishing time", "Back"])
    show_analyze_menu(ask_fn=lambda _: next(choices))
    captured = capsys.readouterr()
    assert "[TODO]" in captured.out
    assert "target" in captured.out.lower()


def test_analyze_back_returns_without_exit():
    choices = iter(["Back"])
    show_analyze_menu(ask_fn=lambda _: next(choices))


def test_analyze_quit_exits():
    choices = iter(["Quit"])
    with pytest.raises(SystemExit):
        show_analyze_menu(ask_fn=lambda _: next(choices))
