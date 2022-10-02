# TODO: this doesn't work here
__all__ = ["static_init","asdict"]

from typing import Protocol, TypeVar

class Proto(Protocol):
    @classmethod
    def static_init(cls):
        pass

P = TypeVar("P", bound=Proto)

def static_init(cls: P) -> P:
    cls.static_init()
    return cls

from dataclasses import asdict as asdict_
from bson.objectid import ObjectId

def asdict(obj, *, dict_factory=dict):
    # TODO: we need to do a deepcheck here
    dict_ = asdict_(obj, dict_factory=dict_factory)
    return {k:(v if isinstance(k,ObjectId) else str(v)) for k,v in dict_.items()}