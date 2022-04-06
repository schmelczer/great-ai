import logging
import random
from pathlib import Path

from good_ai.good_ai.tracing.tracing_context import TracingContext
from good_ai.open_s3 import LargeFile

from .tracing import PersistenceDriver, TinyDbDriver

logger = logging.getLogger("good_ai")

_initialized = False


def set_default_config_if_uninitialized() -> None:
    if not _initialized:
        set_default_config()


def set_default_config(
    log_level: int = logging.INFO,
    s3_config: Path = Path("s3.ini"),
    seed: int = 42,
    tracing_db_driver: PersistenceDriver = TinyDbDriver(Path("tracing_database.json")),
) -> None:
    global _initialized
    logging.basicConfig(level=log_level)

    _initialize_large_file(s3_config)
    _set_seed(seed)

    TracingContext.persistence_driver = tracing_db_driver

    _initialized = True

    logger.info("Defaults: configured ✅")


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
