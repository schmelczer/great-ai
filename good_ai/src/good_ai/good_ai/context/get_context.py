import os
import random
from logging import INFO, Logger
from pathlib import Path
from typing import Optional, cast

from good_ai.open_s3 import LargeFile
from good_ai.utilities.logger import create_logger

from ..persistence import ParallelTinyDbDriver, PersistenceDriver
from .context import Context

_context: Optional[Context] = None
PRODUCTION_KEY = "production"


def get_context() -> Context:
    if _context is None:
        set_default_config()

    return cast(Context, _context)


def set_default_config(
    log_level: int = INFO,
    s3_config: Path = Path("s3.ini"),
    seed: int = 42,
    persistence_driver: PersistenceDriver = ParallelTinyDbDriver(
        Path("tracing_database.json")
    ),
    is_production_mode_override: Optional[bool] = None,
) -> None:
    global _context

    logger = create_logger("good_ai", level=log_level)

    is_production = _is_in_production_mode(
        override=is_production_mode_override, logger=logger
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

    logger.info("Defaults: configured ✅")


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
