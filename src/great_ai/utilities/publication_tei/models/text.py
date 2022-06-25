from typing import Optional

from pydantic import BaseModel


class Text(BaseModel):
    content: str
    document_order: int
    coordinates: Optional[str]
