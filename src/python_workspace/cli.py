from __future__ import annotations

import argparse

from python_workspace.order_analysis import display_report


def greet(name: str = "World") -> str:
    return f"Hello, {name}!"


def main() -> None:
    parser = argparse.ArgumentParser(description="Customer order analysis report.")
    parser.add_argument(
        "name",
        nargs="?",
        help="optionally print a greeting instead of the analysis report",
    )
    args = parser.parse_args()
    if args.name is None:
        display_report()
    else:
        print(greet(args.name))


if __name__ == "__main__":
    main()
