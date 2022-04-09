import logging
import os
import random
from pathlib import Path
from typing import Optional, cast

from good_ai.open_s3 import LargeFile

from ..persistence import PersistenceDriver, TinyDbDriver
from .context import Context

logger = logging.getLogger("good_ai")


_context: Optional[Context] = None
PRODUCTION_KEY = "production"


def get_context() -> Context:
    if _context is None:
        set_default_config()

    return cast(Context, _context)


def set_default_config(
    log_level: int = logging.INFO,
    s3_config: Path = Path("s3.ini"),
    seed: int = 42,
    persistence_driver: PersistenceDriver = TinyDbDriver(Path("tracing_database.json")),
    is_production_mode_override: Optional[bool] = None,
) -> None:
    global _context
    logging.basicConfig(level=log_level)

    is_production = _is_in_production_mode(override=is_production_mode_override)
    _initialize_large_file(s3_config)
    _set_seed(seed)

    is_threadsafe = not isinstance(persistence_driver, TinyDbDriver)
    if not is_threadsafe:
        logger.warn("The selected persistence driver (TinyDbDriver) is not threadsafe")
    _context = Context(
        metrics_path="/metrics",
        persistence=persistence_driver,
        is_production=is_production,
        is_threadsafe=is_threadsafe,
    )

    logger.info("Defaults: configured ✅")


def _is_in_production_mode(override: Optional[bool]) -> bool:
    environment = os.environ.get("ENVIRONMENT", PRODUCTION_KEY).lower()
    is_production = environment == PRODUCTION_KEY if override is None else override

    if is_production:
        logger.info("Running in production mode ✅")
    else:
        logger.warn("Running in development mode ‼️")

    return is_production


def _initialize_large_file(s3_config: Path) -> None:
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
