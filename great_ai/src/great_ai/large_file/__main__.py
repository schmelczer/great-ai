#!/usr/bin/env python3

from pathlib import Path

from great_ai.utilities.logger import get_logger

from .large_file import LargeFileLocal, LargeFileS3
from .parse_arguments import parse_arguments

logger = get_logger("large_file")


def main() -> None:
    parser, args = parse_arguments()

    factory = {"s3": LargeFileS3, "local": LargeFileLocal}

    if args.driver not in factory:
        raise ValueError(
            f"Driver {args.driver} does not exits, available options: {' ,'.join(factory.keys())}"
        )

    large_file = factory[args.driver]

    if args.driver != "local":
        if args.secrets is None:
            raise ValueError(
                "Providing a credentials file is required when the driver mode is not `local`."
            )
        large_file.configure_credentials_from_file(args.secrets)  # type: ignore

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


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        logger.warning("Exiting")
        exit()
    except Exception as e:
        logger.error(e)
