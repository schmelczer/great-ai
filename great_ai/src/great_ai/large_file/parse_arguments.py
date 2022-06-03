from argparse import ArgumentParser, Namespace
from typing import Tuple


def parse_arguments() -> Tuple[ArgumentParser, Namespace]:
    parser = ArgumentParser(
        description="Store and version large files in S3; open them like regular files. Caching included.",
    )

    parser.add_argument(
        "-b",
        "--backend",
        type=str,
        help="choose which backend to use, available options: `local`, `s3`, `mongodb`",
        required=True,
    )

    parser.add_argument(
        "-s",
        "--secrets",
        type=str,
        help="path to an .ini configuration file with your S3 credentials",
        required=False,
    )

    parser.add_argument(
        "-c",
        "--cache",
        nargs="+",
        type=str,
        help="download file into local cache, example: file_name.txt:version",
        required=False,
    )

    parser.add_argument(
        "-p",
        "--push",
        nargs="+",
        type=str,
        help="push a local file into S3 and set it as the most recent version",
        required=False,
    )

    parser.add_argument(
        "-d",
        "--delete",
        nargs="+",
        type=str,
        help="delete every version of file from S3",
        required=False,
    )

    parser.print_usage = parser.print_help  # type: ignore
    args = parser.parse_args()

    return parser, args
