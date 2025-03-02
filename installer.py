import argparse
import dratini.installer as installer


# Create the argument parser.
argument_parser = argparse.ArgumentParser(
        prog="dratini-installer",
        usage="dratini-installer --help",
        description="The CLI installer/uninstaller for Dratini.",
        epilog="Copyright (c) 2025 - bonusbyte.org"
)
# Add flags `--install`.
argument_parser.add_argument(
        "--install",
        action="store_true"
)
# Add flag `--uninstall`.
argument_parser.add_argument(
        "--uninstall",
        action="store_true"
)


def parse_args() -> argparse.Namespace:
    # Parse the arguments.
    return argument_parser.parse_args()


args = parse_args()

if args.install:
    installer.install()
elif args.uninstall:
    installer.uninstall()
else:
    argument_parser.print_help()
