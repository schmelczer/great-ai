import os
import random
from logging import DEBUG, Logger
from pathlib import Path
from typing import Any, Dict, Optional, Type, Union, cast

from pydantic import BaseModel

from great_ai import __version__

from .constants import (
    DEFAULT_LARGE_FILE_CONFIG_PATHS,
    DEFAULT_TRACING_DATABASE_CONFIG_PATHS,
    ENV_VAR_KEY,
    LIST_ITEM_PREFIX,
    PRODUCTION_KEY,
    SE4ML_WEBSITE,
)
from .large_file import LargeFileBase, LargeFileLocal
from .persistence.parallel_tinydb_driver import ParallelTinyDbDriver
from .persistence.tracing_database_driver import TracingDatabaseDriver
from .utilities import get_logger
from .views import RouteConfig


class Context(BaseModel):
    version: Union[int, str]
    tracing_database: TracingDatabaseDriver
    large_file_implementation: Type[LargeFileBase]
    is_production: bool
    logger: Logger
    should_log_exception_stack: bool
    prediction_cache_size: int
    dashboard_table_size: int
    route_config: RouteConfig

    class Config:
        arbitrary_types_allowed = True

    def to_flat_dict(self) -> Dict[str, Any]:
        return {
            "tracing_database": type(self.tracing_database).__name__,
            "large_file_implementation": self.large_file_implementation.__name__,
            "is_production": self.is_production,
            "should_log_exception_stack": self.should_log_exception_stack,
            "prediction_cache_size": self.prediction_cache_size,
            "dashboard_table_size": self.dashboard_table_size,
        }


_context: Optional[Context] = None


def get_context() -> Context:
    if _context is None:
        configure()

    return cast(Context, _context)


def configure(
    *,
    version: Union[int, str] = "0.0.1",
    log_level: int = DEBUG,
    seed: int = 42,
    tracing_database_factory: Optional[Type[TracingDatabaseDriver]] = None,
    large_file_implementation: Optional[Type[LargeFileBase]] = None,
    should_log_exception_stack: Optional[bool] = None,
    prediction_cache_size: int = 512,
    disable_se4ml_banner: bool = False,
    dashboard_table_size: int = 50,
    route_config: RouteConfig = RouteConfig(),
) -> None:
    """Set the global configuration used by the great-ai library.

    You must call `configure` before calling (or decorating with) any other great-ai
    function.

    If `tracing_database_factory` or `large_file_implementation` is not specified, their
    default value is determined based on which TracingDatabase and LargeFile has been
    configured (e.g.: LargeFileS3.configure_credentials_from_file('s3.ini')), or whether
    there is any file named s3.ini or mongo.ini in the working directory.

    Examples:
        >>> configure(prediction_cache_size=0)

    Arguments:
        version: The version of your application (using SemVer is recommended).
        log_level: Set the default logging level of `logging`.
        seed: Set seed of `random` (and `numpy` if installed) for reproducibility.
        tracing_database_factory: Specify a different TracingDatabaseDriver than the one
            already configured.
        large_file_implementation: Specify a different LargeFile than the one already
            configured.
        should_log_exception_stack: Log the traces of unhandled exceptions.
        prediction_cache_size: Size of the LRU cache applied over the prediction
            functions.
        disable_se4ml_banner: Turn off the warning about the importance of SE4ML best-
            practices.
        dashboard_table_size: Number of rows to display in the dashboard's table.
        route_config: Enable or disable specific HTTP API endpoints.
    """

    global _context
    logger = get_logger("great_ai", level=log_level)

    if _context is not None:
        logger.error(
            "Configuration has been already initialised, overwriting.\n"
            + "Make sure to call `configure()` before importing your application code."
        )

    is_production = _is_in_production_mode(logger=logger)

    _set_seed(seed)

    tracing_database_factory = _initialize_tracing_database(
        tracing_database_factory, logger=logger
    )
    tracing_database = tracing_database_factory()

    if not tracing_database.is_production_ready:
        message = f"""The selected tracing database ({
            tracing_database_factory.__name__
        }) is not recommended for production"""

        if is_production:
            logger.error(message)
        else:
            logger.warning(message)

    _context = Context(
        version=version,
        tracing_database=tracing_database,
        large_file_implementation=_initialize_large_file(
            large_file_implementation, logger=logger
        ),
        is_production=is_production,
        logger=logger,
        should_log_exception_stack=not is_production
        if should_log_exception_stack is None
        else should_log_exception_stack,
        prediction_cache_size=prediction_cache_size,
        dashboard_table_size=dashboard_table_size,
        route_config=route_config,
    )

    logger.info(f"GreatAI (v{__version__}): configured ✅")
    for k, v in get_context().to_flat_dict().items():
        logger.info(f"{LIST_ITEM_PREFIX}{k}: {v}")

    if not is_production and not disable_se4ml_banner:
        logger.warning(
            "You still need to check whether you follow all best practices before "
            "trusting your deployment."
        )
        logger.warning(f"> Find out more at {SE4ML_WEBSITE}")


def _is_in_production_mode(logger: Optional[Logger]) -> bool:
    environment = os.environ.get(ENV_VAR_KEY)

    if environment is None:
        if logger:
            logger.warning(
                f"Environment variable {ENV_VAR_KEY} is not set, "
                "defaulting to development mode ‼️"
            )
        is_production = False
    else:
        is_production = environment.lower() == PRODUCTION_KEY
        if logger:
            if not is_production:
                logger.info(
                    f"Value of {ENV_VAR_KEY} is `{environment}` which is not equal to"
                    + f"`{PRODUCTION_KEY}` defaulting to development mode ‼️"
                )
            else:
                logger.info("Running in production mode ✅")

    return is_production


def _initialize_tracing_database(
    selected: Optional[Type[TracingDatabaseDriver]], logger: Logger
) -> Type[TracingDatabaseDriver]:
    for tracing_driver, paths in DEFAULT_TRACING_DATABASE_CONFIG_PATHS.items():
        if selected is None or selected == tracing_driver:
            if tracing_driver.initialized:
                logger.info(
                    f"{tracing_driver.__name__} has been already configured: "
                    "skipping initialisation"
                )
                return tracing_driver
            for p in paths:
                if Path(p).exists():
                    logger.info(
                        f"""Found credentials file ({Path(p).absolute()}), initialising {
                            tracing_driver.__name__
                        }"""
                    )
                    tracing_driver.configure_credentials_from_file(p)
                    return tracing_driver
    logger.warning(
        "Cannot find credentials files, defaulting to using ParallelTinyDbDriver"
    )
    return ParallelTinyDbDriver


def _initialize_large_file(
    selected: Optional[Type[LargeFileBase]], logger: Logger
) -> Type[LargeFileBase]:
    for large_file, paths in DEFAULT_LARGE_FILE_CONFIG_PATHS.items():
        if selected is None or selected == large_file:
            if large_file.initialized:
                logger.info(
                    f"{large_file.__name__} has been already configured: skipping initialisation"
                )
                return large_file
            for p in paths:
                if Path(p).exists():
                    logger.info(
                        f"""Found credentials file ({Path(p).absolute()}), initialising {
                            large_file.__name__
                        }"""
                    )
                    large_file.configure_credentials_from_file(p)
                    return large_file
    logger.warning("Cannot find credentials files, defaulting to using LargeFileLocal")
    return LargeFileLocal


def _set_seed(seed: int) -> None:
    random.seed(seed)

    try:
        import numpy

        numpy.random.seed(seed + 1)
    except ImportError:
        pass
