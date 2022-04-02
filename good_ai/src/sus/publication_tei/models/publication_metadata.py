from typing import List, Optional

from pydantic import BaseModel


class PublicationMetadata(BaseModel):
    language: Optional[str]
    title: Optional[str]
    publisher: Optional[str]
    doi: Optional[str]
    md5: Optional[str]
    publication_date: Optional[str]
    keywords: List[str]
    reference_count: int
