from pydantic import BaseModel


class HashableBaseModel(BaseModel):
    def __hash__(self) -> int:
        from ..helper.frozen_call import make_hashable

        return hash(make_hashable(self))
