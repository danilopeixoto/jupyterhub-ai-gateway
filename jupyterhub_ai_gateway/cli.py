"""
Command-line interface module.
"""

import argparse

import uvicorn

from .app import create_app
from .settings import settings


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
        default=settings.jupyterhub_ai_gateway_config,
        help="Path to configuration file. Defaults to config.yaml.",
    )
    parser.add_argument(
        "-m",
        "--metrics",
        action="store_true",
        default=settings.jupyterhub_ai_gateway_metrics,
        help="Enable server metrics. Defaults to false.",
    )

    args = parser.parse_args()
    app = create_app(args.config, args.metrics)

    uvicorn.run(app, host=args.host, port=args.port)


if __name__ == "__main__":
    main()
