import os
import random
from logging import INFO, Logger
from pathlib import Path

import great_ai.great_ai.context.context as context
from great_ai.open_s3 import LargeFile
from great_ai.utilities.logger import create_logger

from ..constants import DEFAULT_TRACING_DB_FILENAME, ENV_VAR_KEY, PRODUCTION_KEY
from ..persistence import ParallelTinyDbDriver, PersistenceDriver


def configure(
    log_level: int = INFO,
    s3_config: Path = Path("s3.ini"),
    seed: int = 42,
    persistence_driver: PersistenceDriver = ParallelTinyDbDriver(
        Path(DEFAULT_TRACING_DB_FILENAME)
    ),
) -> None:
    logger = create_logger("great_ai", level=log_level)

    if context._context is not None:
        logger.warn(
            "Configuration has been already initialised, overwriting.\n"
            + 'Make sure to call "configure()" before importing your application code.'
        )

    is_production = _is_in_production_mode(
        logger=logger,
    )
    _initialize_large_file(s3_config, logger=logger)
    _set_seed(seed)

    if not persistence_driver.is_threadsafe:
        logger.warning(
            f"The selected persistence driver ({type(persistence_driver).__name__}) is not threadsafe"
        )

    context._context = context.Context(
        metrics_path="/metrics",
        persistence=persistence_driver,
        is_production=is_production,
        logger=logger,
    )

    logger.info("Options: configured ✅")


def _is_in_production_mode(logger: Logger) -> bool:
    environment = os.environ.get(ENV_VAR_KEY)

    if environment is None:
        logger.info(
            f"Environment variable {ENV_VAR_KEY} is not set, defaulting to development mode"
        )
        is_production = False
    else:
        is_production = environment.lower() == PRODUCTION_KEY
        if not is_production:
            logger.info(
                f"Value of {ENV_VAR_KEY} is `{environment}` which is not equal to `{PRODUCTION_KEY}`"
            )

    if is_production:
        logger.info("Running in production mode ✅")
    else:
        logger.warning("Running in development mode ‼️")

    return is_production


def _initialize_large_file(s3_config: Path, logger: Logger) -> None:
    if s3_config.exists():
        LargeFile.configure_credentials_from_file(s3_config)
    else:
        logger.warning(
            f"Provided S3 config ({s3_config.resolve()}) not found, skipping LargeFile initialisation"
        )


def _set_seed(seed: int) -> None:
    random.seed(seed)

    try:
        import numpy

        numpy.random.seed(seed + 1)
    except ImportError:
        pass
