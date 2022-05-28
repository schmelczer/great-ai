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

    parser.add_argument(
        "--host",
        type=str,
        help="it is passed to uvicorn which starts a server listening on this address",
        default="0.0.0.0",
        required=False,
    )

    parser.add_argument(
        "--port",
        type=int,
        help="it is passed to uvicorn which starts a server listening on this port",
        default=6060,
        required=False,
    )

    parser.add_argument(
        "--timeout_keep_alive",
        type=int,
        help="it is passed to uvicorn which uses it for timing out requests taking longer than this many seconds",
        default=600,
        required=False,
    )

    parser.add_argument(
        "--workers",
        type=int,
        help="it is passed to uvicorn which starts this many server processes",
        default=1,
        required=False,
    )

    return parser.parse_args()
