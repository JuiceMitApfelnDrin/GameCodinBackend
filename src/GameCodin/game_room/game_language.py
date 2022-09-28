from __future__ import annotations
from enum import Enum
from typing import ClassVar
from dataclasses import dataclass
from ..utils import static_init
from . import piston

@static_init
@dataclass
class Language:
    __languages: ClassVar[dict[str, Language]]

    name: str
    version: str
    aliases: list[str]
    runtime: str

    @classmethod
    def static_init(cls):
        cls.__languages = {}
        languages: dict[str,dict] = piston.languages

        for lang_name, lang_infos in languages.items():
            lang_version = lang_infos["version"]
            lang_aliases = lang_infos["aliases"]
            lang_runtime = lang_infos.get("runtime","")

            if  not all((type(lang_name) is str,
                        type(lang_version) is str,
                        type(lang_aliases) is list[str],
                        type(lang_runtime) is str)):

                raise TypeError("Piston API: wrong response type")

            # Do we really want to allow all languages ?
            # There is probably rate limits

            language = cls(lang_name, lang_version, lang_aliases, lang_runtime)
            cls.__languages[language.name] = language

    @classmethod
    def get(cls, name: str):
        return cls.__languages[name]
