import os
import random
from logging import INFO, Logger
from pathlib import Path
from typing import Optional, cast

from great_ai.open_s3 import LargeFile
from great_ai.utilities.logger import create_logger

from ..persistence import ParallelTinyDbDriver, PersistenceDriver
from .context import Context

_context: Optional[Context] = None
PRODUCTION_KEY = "production"


def get_context() -> Context:
    if _context is None:
        configure()

    return cast(Context, _context)


def configure(
    log_level: int = INFO,
    s3_config: Path = Path("s3.ini"),
    seed: int = 42,
    persistence_driver: PersistenceDriver = ParallelTinyDbDriver(
        Path("tracing_database.json")
    ),
    development_mode_override: Optional[bool] = None,
) -> None:
    global _context

    logger = create_logger("great_ai", level=log_level)

    if _context is not None:
        logger.warn(
            "Configuration has been already initialised, overwriting.\n"
            + 'Make sure to call "configure()" before importing your application code.'
        )

    is_production = _is_in_production_mode(
        override=None
        if development_mode_override is None
        else not development_mode_override,
        logger=logger,
    )
    _initialize_large_file(s3_config, logger=logger)
    _set_seed(seed)

    if not persistence_driver.is_threadsafe:
        logger.warning(
            f"The selected persistence driver ({type(persistence_driver).__name__}) is not threadsafe"
        )
    _context = Context(
        metrics_path="/metrics",
        persistence=persistence_driver,
        is_production=is_production,
        logger=logger,
    )

    logger.info("Options: configured ✅")


def _is_in_production_mode(override: Optional[bool], logger: Logger) -> bool:
    environment = os.environ.get("ENVIRONMENT", PRODUCTION_KEY).lower()
    is_production = environment == PRODUCTION_KEY if override is None else override

    if is_production:
        logger.info("Running in production mode ✅")
    else:
        logger.warning("Running in development mode ‼️")

    return is_production


def _initialize_large_file(s3_config: Path, logger: Logger) -> None:
    if s3_config.exists():
        LargeFile.configure_credentials_from_file(s3_config)
    else:
        logger.info(
            f"Provided S3 config ({s3_config.resolve()}) not found, skipping LargeFile initialisation"
        )


def _set_seed(seed: int) -> None:
    random.seed(seed)
    try:
        import numpy

        numpy.random.seed(seed + 1)
    except ImportError:
        pass
