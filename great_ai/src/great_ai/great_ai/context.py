import os
import random
from logging import DEBUG, Logger
from pathlib import Path
from typing import Any, Dict, Optional, Type, cast

from pydantic import BaseModel

from great_ai.large_file import LargeFile, LargeFileLocal
from great_ai.utilities.logger import get_logger
import yaml
from .constants import (
    DEFAULT_LARGE_FILE_CONFIG_PATHS,
    DEFAULT_TRACING_DB_FILENAME,
    ENV_VAR_KEY,
    PRODUCTION_KEY,
    SE4ML_WEBSITE,
)
from .persistence import ParallelTinyDbDriver, TracingDatabaseDriver


class Context(BaseModel):
    tracing_database: TracingDatabaseDriver
    large_file_implementation: Type[LargeFile]
    is_production: bool
    logger: Logger
    should_log_exception_stack: bool
    prediction_cache_size: int

    class Config:
        arbitrary_types_allowed = True

    def to_flat_dict(self) -> Dict[str, Any]:
        return {
            "tracing_database": type(self.tracing_database).__name__,
            "large_file_implementation": self.large_file_implementation.__name__,
            "is_production": self.is_production,
            "should_log_exception_stack": self.should_log_exception_stack,
            "prediction_cache_size": self.prediction_cache_size,
        }


_context: Optional[Context] = None


def get_context() -> Context:
    if _context is None:
        configure()

    return cast(Context, _context)


def configure(
    *,
    log_level: int = DEBUG,
    seed: int = 42,
    tracing_database: TracingDatabaseDriver = ParallelTinyDbDriver(
        Path(DEFAULT_TRACING_DB_FILENAME)
    ),
    large_file_implementation: Type[LargeFile] = LargeFileLocal,
    should_log_exception_stack: Optional[bool] = None,
    prediction_cache_size: int = 512,
    disable_se4ml_banner: bool=False
) -> None:
    global _context
    logger = get_logger("great_ai", level=log_level)

    if _context is not None:
        logger.warn(
            "Configuration has been already initialised, overwriting.\n"
            + "Make sure to call `configure()` before importing your application code."
        )

    is_production = _is_in_production_mode(logger=logger)
    _initialize_large_file(large_file_implementation, logger=logger)
    _set_seed(seed)

    if not tracing_database.is_production_ready:
        if is_production:
            logger.error(
                f"The selected tracing database ({type(tracing_database).__name__}) is not recommended for production"
            )
        else:
            logger.warning(
                f"The selected tracing database ({type(tracing_database).__name__}) is not recommended for production"
            )

    _context = Context(
        tracing_database=tracing_database,
        large_file_implementation=large_file_implementation,
        is_production=is_production,
        logger=logger,
        should_log_exception_stack=not is_production
        if should_log_exception_stack is None
        else should_log_exception_stack,
        prediction_cache_size=prediction_cache_size,
    )

    logger.info("Setting: configured ✅")
    for k, v in get_context().to_flat_dict().items():
        logger.info(f'🔩 {k}: {v}')

    if not is_production and not disable_se4ml_banner:
        logger.warning(f'You still need to check whether you follow all best practices so that you and others can trust your deployment.')
        logger.warning(f'> Find out more at {SE4ML_WEBSITE}')



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


def _initialize_large_file(large_file: Type[LargeFile], logger: Logger) -> None:
    path = DEFAULT_LARGE_FILE_CONFIG_PATHS[large_file]
    if path is None:
        return

    if large_file.initialized:
        logger.warning(
            f"{large_file.__name__} has been already configured: skipping initialisation"
        )
        return

    if path.exists():
        large_file.configure_credentials_from_file(path)
        logger.info(f"{large_file.__name__} initialised with config ({path.resolve()})")
    else:
        logger.warning(
            f"Default {large_file.__name__} config ({path.resolve()}) not found, skipping {large_file.__name__} initialisation"
        )


def _set_seed(seed: int) -> None:
    random.seed(seed)

    try:
        import numpy

        numpy.random.seed(seed + 1)
    except ImportError:
        pass
