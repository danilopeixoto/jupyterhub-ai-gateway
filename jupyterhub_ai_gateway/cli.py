"""
Command-line interface module.
"""

import argparse

import uvicorn

from .app import create_app


def main():
    """
    Start service application.
    """

    parser = argparse.ArgumentParser(description="AI gateway service for JupyterHub.")

    parser.add_argument(
        "-H",
        "--host",
        type=str,
        default="localhost",
        help="The service hostname. Defaults to localhost.",
    )
    parser.add_argument(
        "-p",
        "--port",
        type=int,
        default=5000,
        help="The service port. Defaults to 5000.",
    )
    parser.add_argument(
        "-c",
        "--config",
        type=str,
        default="config.yaml",
        help="Path to configuration file. Defaults to config.yaml.",
    )

    args = parser.parse_args()
    app = create_app(args.config)

    uvicorn.run(app, host=args.host, port=args.port)


if __name__ == "__main__":
    main()
