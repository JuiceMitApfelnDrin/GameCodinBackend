from __future__ import annotations

from dataclasses import dataclass, field
from distutils.log import info
from typing import Any, ClassVar, Optional, cast
from bson.objectid import ObjectId
from uuid import uuid4

from .profile import Profile
from . import users_collection

# TODO: make username and email unique for each user

# TODO: for version 0.2.0:
# profile: Profile

@dataclass(eq=False, kw_only=True)
class User:
    __current_users: ClassVar[dict[ObjectId, User]] = {}

    _id: ObjectId
    username: str
    email: str
    password: str
    token: str

    __ref_count: int = field(init=False, default=0)

    @classmethod
    def create(cls, username: str, email: str, password: str) -> Optional[User]:
        result = users_collection.insert_one(
            {
                "username": username,
                "email": email,
                "password": password,
                "token": uuid4().hex,
            }
        )
        user = User.get_by_id(result.inserted_id)
        return user

    @classmethod
    def get_by_id(cls, user_id: ObjectId) -> Optional[User]:
        if id in cls.__current_users:
            return cls.__current_users[user_id]

        info = cls.__get_info_from_db(user_id)
        if info is None:
            return
        return User.from_dict(info)

    @classmethod
    def __get_info_from_db(cls, user_id: ObjectId) -> Optional[dict]:
        return cast(dict, users_collection.find_one({"_id": user_id}))

    @classmethod
    def from_dict(cls, infos: dict) -> User:
        return cls(
            _id = ObjectId(infos["_id"]), username = infos["username"],
            password = infos["password"], email = infos["email"], token = infos["token"])

    @property
    def id(self):
        return self._id

    def as_dict(self) -> dict[str, Any]:
        return {
            "_id": str(self.id),
            "username": self.username,
            "email": self.email,
            "password": self.password,
            "token": self.token
        }

    def public_info(self) -> dict[str, Any]:
        return {
            "_id": str(self.id),
            "username": self.username
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
