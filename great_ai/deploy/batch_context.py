import copy
import os
from typing import Any, Dict

import dill

from .. import context
from ..utilities import get_logger


class BatchContext:
    """Carry application configuration into independently bootstrapped workers."""

    def __init__(self) -> None:
        current = context.get_context()
        values: Dict[str, Any] = {
            name: getattr(current, name) for name in context.Context.model_fields
        }
        database = copy.copy(current.tracing_database)
        # Built-in drivers allow configuration on their class as well as instance.
        for name in ("path_to_db", "mongo_connection_string", "mongo_database"):
            if hasattr(database, name):
                setattr(database, name, getattr(database, name))
        values["tracing_database"] = database
        values["logger"] = (current.logger.name, current.logger.level)
        implementation = current.large_file_implementation
        storage = {
            name: getattr(implementation, name)
            for name in (
                "cache_path",
                "max_cache_size",
                "initialized",
                *implementation._configuration_attributes,
            )
        }
        self._configuration = dill.dumps((values, storage))
        self._parent_pid = os.getpid()
        self._restored = False

    def restore(self) -> None:
        if os.getpid() == self._parent_pid or self._restored:
            return
        values, storage = dill.loads(self._configuration)
        name, level = values["logger"]
        values["logger"] = get_logger(name, level=level)
        implementation = values["large_file_implementation"]
        for name, value in storage.items():
            setattr(implementation, name, value)
        context._context = context.Context(**values)
        self._restored = True
