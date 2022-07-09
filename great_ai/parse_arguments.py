from argparse import ArgumentParser, Namespace


def parse_arguments() -> Namespace:
    parser = ArgumentParser(
        description="GreatAI-Server for deploying you AI applications with ease.",
    )

    parser.add_argument(
        "file_name",
        type=str,
        help="the name of the file containing your to-be-served function such as `main.py`\n",
    )

    default_host = "0.0.0.0"
    parser.add_argument(
        "--host",
        type=str,
        help=f"it is passed to uvicorn which starts a server listening on this address (default: {default_host})",
        default=default_host,
        required=False,
    )

    default_port = 6060
    parser.add_argument(
        "--port",
        type=int,
        help=f"it is passed to uvicorn which starts a server listening on this port (default: {default_port})",
        default=default_port,
        required=False,
    )

    default_timeout_keep_alive = 600
    parser.add_argument(
        "--timeout_keep_alive",
        type=int,
        help=f"it is passed to uvicorn which uses it for timing out requests taking longer than this many seconds (default: {default_timeout_keep_alive})",
        default=600,
        required=False,
    )

    default_worker_count = 1
    parser.add_argument(
        "--worker_count",
        type=int,
        help=f"it is passed to uvicorn which starts this many server processes (default: {default_worker_count})",
        default=default_worker_count,
        required=False,
    )

    return parser.parse_args()
