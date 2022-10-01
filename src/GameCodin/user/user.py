from __future__ import annotations

from dataclasses import dataclass, asdict, field
from distutils.log import info
from typing import ClassVar, Optional, cast
from bson.objectid import ObjectId

from ..database.collection import Collection
from .profile import Profile
from ..database import db_client

from uuid import uuid4

# TODO: make username and email unique for each user

@dataclass
class User:
    __current_users: ClassVar[dict[ObjectId, User]] = {}

    user_id: ObjectId
    username: str
    email: str
    user_token: str

    # TODO: for version 2.0:
    # profile: Profile

    @property
    def dict(self) -> dict:
        infos = asdict(self)
        infos["user_id"] = str(self.user_id)
        return infos

    @classmethod
    def create(cls, username, email) -> User:
        result = db_client[Collection.USERS.value].insert_one(
            {
                "username": username,
                "email": email,
                "user_token": uuid4().hex,
            }
        )
        user = User.get_by_id(result.inserted_id)
        assert user is not None
        return user

    @classmethod
    def get_by_id(cls, user_id: ObjectId) -> Optional[User]:
        if user_id in cls.__current_users:
            return cls.__current_users[user_id]

        user_info = cls.__get_user_info_from_db(user_id)
        if user_info is None:
            return
        return User.from_dict(user_info)

    @classmethod
    def __get_user_info_from_db(cls, user_id: ObjectId) -> Optional[dict]:
        return cast(dict, db_client[Collection.USERS.value].find_one({"_id": user_id}))

    @classmethod
    def from_dict(cls, infos: dict) -> User:
        return cls(infos["_id"], infos["username"], infos["email"], infos["user_token"])

    def __post_init__(self):
        self.__ref_count = 0

    @property
    def ref_count(self):
        return self.__ref_count

    def acquire(self):
        if not self.__ref_count:
            self.__current_users[self.user_id] = self
        self.__ref_count += 1

    def release(self):
        self.__ref_count -= 1
        if not self.__ref_count:
            del self.__current_users[self.user_id]
