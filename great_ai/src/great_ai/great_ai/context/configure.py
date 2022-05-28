import os
import random
from logging import DEBUG, Logger
from pathlib import Path
from typing import Optional

import great_ai.great_ai.context.context as context
from great_ai.open_s3 import LargeFile
from great_ai.utilities.logger import get_logger

from ..constants import DEFAULT_TRACING_DB_FILENAME, ENV_VAR_KEY, PRODUCTION_KEY
from ..persistence import ParallelTinyDbDriver, PersistenceDriver


def configure(
    version: str = "0.0.1",
    log_level: int = DEBUG,
    s3_config: Path = Path("s3.ini"),
    seed: int = 42,
    persistence_driver: PersistenceDriver = ParallelTinyDbDriver(
        Path(DEFAULT_TRACING_DB_FILENAME)
    ),
    should_log_exception_stack: Optional[bool] = None,
    prediction_cache_size: int = 512,
) -> None:
    logger = get_logger("great_ai", level=log_level)

    if context._context is not None:
        logger.warn(
            "Configuration has been already initialised, overwriting.\n"
            + 'Make sure to call "configure()" before importing your application code.'
        )

    is_production = _is_in_production_mode(logger=logger)
    _initialize_large_file(s3_config, logger=logger)
    _set_seed(seed)

    if not persistence_driver.is_threadsafe:
        logger.warning(
            f"The selected persistence driver ({type(persistence_driver).__name__}) is not threadsafe"
        )

    context._context = context.Context(
        version=version,
        persistence=persistence_driver,
        is_production=is_production,
        logger=logger,
        should_log_exception_stack=not is_production
        if should_log_exception_stack is None
        else should_log_exception_stack,
        prediction_cache_size=prediction_cache_size,
    )

    logger.info("Options: configured ✅")


def _is_in_production_mode(logger: Optional[Logger]) -> bool:
    environment = os.environ.get(ENV_VAR_KEY)

    if environment is None:
        if logger:
            logger.warning(
                f"Environment variable {ENV_VAR_KEY} is not set, defaulting to development mode ‼️"
            )
        is_production = False
    else:
        is_production = environment.lower() == PRODUCTION_KEY
        if logger:
            if not is_production:
                logger.info(
                    f"Value of {ENV_VAR_KEY} is `{environment}` which is not equal to `{PRODUCTION_KEY}`"
                    + "defaulting to development mode ‼️"
                )
            else:
                logger.info("Running in production mode ✅")

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
