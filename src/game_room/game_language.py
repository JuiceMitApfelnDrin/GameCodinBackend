from __future__ import annotations
from enum import Enum
from typing import ClassVar
from dataclasses import dataclass


@dataclass
class Language(Enum):
    __languages: ClassVar[dict[str, Language]]

    name: str
    value: int

    @classmethod
    def static_init(cls):
        cls.__languages = {}
        # TODO: we need to parse language infos
        languages = []
        for language_infos in languages:
            # A change in the piston API can break our code KEKW
            language = cls(*language_infos, value=len(cls.__languages))
            cls.__languages[language.name] = language

    # language gets auto added to dict PogU? Might not be the safest idea LUL ---shhhhh
    # def __post_init__(self):
    #    self.value = len(self.__languages)
    #    self.__languages[self.name] = self

    @classmethod
    def get(cls, name: str):
        return cls.__languages[name]
