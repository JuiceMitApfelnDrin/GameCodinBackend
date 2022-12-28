from __future__ import annotations

import re
from typing import Any, ClassVar, Optional, cast, Final

from dataclasses import dataclass, field
from bson.objectid import ObjectId

from .profile import Profile
from . import users_collection, UserCreationException

from bcrypt import gensalt, hashpw, checkpw
from base64 import b64encode, b64decode


# TODO: for version 0.2.0:
# profile: Profile
# allow options for certain queries e.g.: get_by_nickname (amount of users returned)

# XXX: Password/token stuff + User.create are WIP! Didn't test them!

@dataclass(eq=False, kw_only=True)
class User:
    __current_users: ClassVar[dict[ObjectId, User]] = {}

    _id: ObjectId
    nickname: str
    email: str
    password: bytes
    token: bytes

    __ref_count: int = field(init=False, default=0)

    @classmethod
    def create(cls, nickname: str, email: str, password: str) -> tuple[User, str]:
        """
        WIP! Didn't test this
        returns user, token
        """

        if not 8 <= len(password) <= 256:
            raise UserCreationException("Password must be between 8 and 256 characters")

        if not 3 <= len(nickname) <= 32:
            raise UserCreationException("Nickname must be between 3 and 32 characters")
        
        if re.match(r"^[A-Za-z0-9_.\-]+$", nickname):
            raise UserCreationException("Nickname allowed characters are A-Z a-z 0-9 _ . -")


        user = User(
            _id=ObjectId(),
            nickname=nickname,
            email=email,
            password=b"",
            token=b"")

        token = user.set_password(password)

        result = users_collection.insert_one(
            {
                "nickname": user.nickname,
                "email": user.email,
                "password": user.password,
                "token": user.token
            }
        )

        user._id = result.inserted_id

        return user, token

    @classmethod
    def get_by_id(cls, user_id: ObjectId) -> Optional[User]:
        if user_id in cls.__current_users:
            return cls.__current_users[user_id]

        info = cls.__get_info_from_db(user_id)
        if info is None:
            return
        return User.from_dict(info)

    @classmethod
    def __get_info_from_db(cls, user_id: ObjectId) -> Optional[dict]:
        return cast(dict, users_collection.find_one({"_id": user_id}))

    @classmethod
    def get_list_by_nickname(cls, nicknameIncludes: str) -> list[User]:
        """
        Retrieves (currently max 5) users that include a certain string in their nickname from the database
        then those users are transformed into User objects
        """
        # currently I would opt for max 5, can be larger later, alternatively send an option for the size

        pipeline = {
            "nickname": {
                "$regex": nicknameIncludes, "$options": 'i'
            }
        }
        users_information = list(users_collection.find(
            pipeline
        ).limit(5))

        users = []
        for user in users_information:
            users.append(User.from_dict(user))

        return users

    @classmethod
    def get_by_nickname(cls, nickname: str) -> Optional[User]:
        info = users_collection.find_one({"nickname": nickname})

        if info is None:
            return

        return User.from_dict(info)

    @classmethod
    def get_by_email(cls, email: str) -> Optional[User]:
        info = users_collection.find_one({"email": email})

        if info is None:
            return

        return User.from_dict(info)

    @classmethod
    def from_dict(cls, infos: dict) -> User:
        return cls(
            _id=ObjectId(infos["_id"]), nickname=infos["nickname"],
            password=infos["password"], email=infos["email"], token=infos["token"])

    @property
    def id(self):
        return self._id

    def set_password(self, password: str) -> str:
        """
        returns a new token
        """
        password_utf8 = password.encode("utf-8")
        self.password = hashpw(password_utf8, gensalt())
        new_token = hashpw(password_utf8, gensalt())
        self.token = hashpw(password_utf8, gensalt())
        return b64encode(new_token).decode()

    def verify_password(self, password: str) -> tuple[bool, str]:
        if not checkpw(password.encode("utf-8"), self.password):
            return False, ""

        password_utf8 = password.encode("utf-8")
        token = hashpw(password_utf8, gensalt())

        return True, b64encode(token).decode()

    def verify_token(self, token: str) -> bool:
        return checkpw(b64decode(token), self.token)

    def as_dict(self) -> dict[str, Any]:
        return {
            "_id": str(self.id),
            "nickname": self.nickname,
            "email": self.email,
            "password": self.password,
            "token": self.token
        }

    def public_info(self) -> dict[str, Any]:
        return {
            "_id": str(self.id),
            "nickname": self.nickname
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
