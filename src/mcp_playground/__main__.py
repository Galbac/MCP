import argparse

from src.mcp_playground.app import mcp
from src.mcp_playground.config import settings
from src.mcp_playground.logging import setup_logging


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--transport",
        choices=("stdio", "sse", "streamable-http"),
        default="stdio",
    )
    parser.add_argument("--mount-path", default=None)
    args = parser.parse_args()

    setup_logging(settings.debug)
    mcp.run(args.transport, mount_path=args.mount_path)


if __name__ == "__main__":
    main()
