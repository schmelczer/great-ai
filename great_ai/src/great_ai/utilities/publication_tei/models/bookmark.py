from pydantic import BaseModel

from .bookmark_title import BookmarkTitle


class Bookmark(BaseModel):
    title: BookmarkTitle
    original_title: str
    document_order: int
    coordinates: str
