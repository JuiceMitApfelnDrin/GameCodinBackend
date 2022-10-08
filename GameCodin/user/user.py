from __future__ import annotations

from dataclasses import dataclass, field
from distutils.log import info
from typing import ClassVar, Optional, cast
from bson.objectid import ObjectId
from uuid import uuid4

from GameCodin.database.collection import Collection
from .profile import Profile
from ..database import db_client


# TODO: make username and email unique for each user

# TODO: for version 0.2.0:
# profile: Profile

@dataclass
class User:
    __current_users: ClassVar[dict[ObjectId, User]] = {}

    _id: ObjectId
    username: str
    email: str
    token: str

    __ref_count: int = field(init=False, default=0)

    @classmethod
    def create(cls, username, email) -> Optional[User]:
        result = db_client[Collection.USERS.value].insert_one(
            {
                "username": username,
                "email": email,
                "token": uuid4().hex,
            }
        )
        user = User.get_by_id(result.inserted_id)
        return user

    @classmethod
    def get_by_id(cls, id: ObjectId) -> Optional[User]:
        if id in cls.__current_users:
            return cls.__current_users[id]

        info = cls.__get_info_from_db(id)
        if info is None:
            return
        return User.from_dict(info)

    @classmethod
    def __get_info_from_db(cls, id: ObjectId) -> Optional[dict]:
        return cast(dict, db_client[Collection.USERS.value].find_one({"_id": id}))

    @classmethod
    def from_dict(cls, infos: dict) -> User:
        return cls(ObjectId(infos.get("_id") or infos["id"]),
                   infos["username"], infos["email"], infos["token"])

    @property
    def id(self):
        return self._id

    def as_dict(self) -> dict:
        return {
            "_id": self.id,
            "username": self.username,
            "email": self.email,
            "token": self.token
        }

    def ref_count(self):
        return self.__ref_count

    def acquire(self):
        if not self.__ref_count:
            self.__current_users[self.id] = self
        self.__ref_count += 1

    def release(self):
        self.__ref_count -= 1
        if not self.__ref_count:
            del self.__current_users[self.id]
