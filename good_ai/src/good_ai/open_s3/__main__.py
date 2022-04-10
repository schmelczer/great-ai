#!/usr/bin/env python3

from pathlib import Path

from good_ai.utilities.logger import create_logger

from .large_file import LargeFile
from .parse_arguments import parse_arguments

if __name__ == "__main__":
    logger = create_logger("open_s3")
    parser, args = parse_arguments()

    LargeFile.configure_credentials_from_file(args.secrets)

    if not args.cache and not args.push and not args.delete:
        logger.warning("No action required.")
        parser.print_help()
    try:
        if args.cache:
            for c in args.cache:
                split = c.split(":")
                file_name = split[0]
                version = None if len(split) == 1 else int(split[1])
                LargeFile(file_name, "r", version=version).get()

        if args.push:
            for p in args.push:
                path = Path(p)
                LargeFile(path.name, "w").push(path)

        if args.delete:
            for f in args.delete:
                LargeFile(f).delete()
    except Exception as e:
        logger.error(e)
