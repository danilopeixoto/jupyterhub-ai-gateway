import argparse

import uvicorn


def main():
    parser = argparse.ArgumentParser(
        description="AI gateway service for JupyterHub."
    )

    parser.add_argument(
        "--hostname",
        type=str,
        default="localhost",
        help="The service hostname."
    )

    parser.add_argument(
        "--port",
        type=int,
        default=8000,
        help="The service port."
    )

    parser.add_argument(
        "--config",
        type=str,
        help="Path to configuration file."
    )

    args = parser.parse_args()

    uvicorn.run("service:app", host=args.host, port=args.port)


if __name__ == "__main__":
    main()
