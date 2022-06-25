#!/usr/bin/env python3

from argparse import Namespace
from pathlib import Path
from typing import Mapping, Type

from ..utilities import get_logger
from .large_file import LargeFile, LargeFileLocal, LargeFileMongo, LargeFileS3
from .parse_arguments import parse_arguments

logger = get_logger("large_file")


def main() -> None:
    parser, args = parse_arguments()

    large_file = get_class(args)

    if not args.cache and not args.push and not args.delete:
        logger.warning("No action required.")
        parser.print_help()

    if args.cache:
        for c in args.cache:
            split = c.split(":")
            file_name = split[0]
            version = None if len(split) == 1 else int(split[1])
            large_file(file_name, "r", version=version).get()

    if args.push:
        for p in args.push:
            path = Path(p)
            large_file(path.name, "w").push(path)

    if args.delete:
        for f in args.delete:
            large_file(f).delete()


def get_class(args: Namespace) -> Type[LargeFile]:
    factory: Mapping[str, Type[LargeFile]] = {
        "s3": LargeFileS3,
        "local": LargeFileLocal,
        "mongodb": LargeFileMongo,
    }

    if args.backend not in factory:
        raise ValueError(
            f"Backend {args.backend} does not exits, available options: {' ,'.join(factory.keys())}"
        )

    large_file = factory[args.backend]

    if args.backend != "local":
        if args.secrets is None:
            raise ValueError(
                "Providing a credentials file is required when the backend mode is not `local`."
            )
        large_file.configure_credentials_from_file(args.secrets)

    return large_file


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        logger.warning("Exiting")
        exit()
    except Exception as e:
        logger.exception(e)
