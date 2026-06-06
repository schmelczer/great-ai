from abc import ABC, abstractmethod
from datetime import datetime
from pathlib import Path
from typing import List, Optional, Sequence, Tuple, Union

from ..utilities import ConfigFile
from ..views import Filter, SortBy, Trace


class TracingDatabaseDriver(ABC):
    """Interface expected from a database to be used for storing traces."""

    is_production_ready: bool
    initialized: bool = False

    @classmethod
    def configure_credentials_from_file(
        cls,
        secrets: Union[Path, str, ConfigFile],
    ) -> None:
        if not isinstance(secrets, ConfigFile):
            secrets = ConfigFile(secrets)
        cls.configure_credentials(**{k.lower(): v for k, v in secrets.items()})

    @classmethod
    def configure_credentials(
        cls,
    ) -> None:
        cls.initialized = True

    @abstractmethod
    def save(self, document: Trace) -> str:
        pass

    @abstractmethod
    def save_batch(
        self,
        documents: List[Trace],
    ) -> List[str]:
        pass

    @abstractmethod
    def get(self, id: str) -> Optional[Trace]:
        pass

    @abstractmethod
    def query(
        self,
        *,
        skip: int = 0,
        take: Optional[int] = None,
        conjunctive_filters: Sequence[Filter] = [],
        conjunctive_tags: Sequence[str] = [],
        until: Optional[datetime] = None,
        since: Optional[datetime] = None,
        has_feedback: Optional[bool] = None,
        sort_by: Sequence[SortBy] = [],
    ) -> Tuple[List[Trace], int]:
        pass

    @abstractmethod
    def update(self, id: str, new_version: Trace) -> None:
        pass

    @abstractmethod
    def delete(self, id: str) -> None:
        pass

    @abstractmethod
    def delete_batch(
        self,
        ids: List[str],
    ) -> None:
        pass
