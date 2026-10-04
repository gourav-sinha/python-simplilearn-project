import sys

from python_workspace.cli import greet, main


def test_greet_default():
    assert greet() == "Hello, World!"


def test_greet_custom_name():
    assert greet("Copilot") == "Hello, Copilot!"


def test_main_defaults_to_analysis_report(monkeypatch, capsys):
    monkeypatch.setattr(sys, "argv", ["python-workspace"])

    main()

    assert "CUSTOMER ORDER ANALYSIS REPORT" in capsys.readouterr().out


def test_main_preserves_positional_greeting(monkeypatch, capsys):
    monkeypatch.setattr(sys, "argv", ["python-workspace", "Copilot"])

    main()

    assert capsys.readouterr().out.strip() == "Hello, Copilot!"
