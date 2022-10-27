from typing import Any

from sanic import text, json, response
from sanic.request import Request

from bson.objectid import ObjectId
from bson.errors import InvalidId
from pymongo.errors import DuplicateKeyError

from validate_email import validate_email
from urllib.parse import urlencode

from ..user import User
from . import app


@app.get('/users')
async def users(request: Request):
    args = request.args
    if "id" in args:
        try:
            user = User.get_by_id(ObjectId(args["id"][0]))
        except InvalidId:
            user = None

        if user is None:
            return text("Can't find user", status=400)

        return json(user.public_info())

    if "substringInNickname" in args:
        try:
            users = User.get_by_substring_in_nickname(
                str(args["substringInNickname"][0]))
        except:
            users = []

        transformed_users = []
        for user in users:
            transformed_users.append(user.public_info())

        return json(transformed_users)

    if "nickname" in args:
        user = User.get_by_nickname(str(args["nickname"][0]))
        if user is None:
            return text(f"User with nickname {args['nickname'][0]} couldn't be found")

        return json(user.public_info())

    if "email" in args:
        user = User.get_by_email(str(args["email"][0]))
        if user is None:
            return text(f"User with email {args['email'][0]} couldn't be found")

        return json(user.public_info())

    return text("Not yet implemented", status=400)


# WIP! Didn't test this at all!
@app.post('/register')
async def register(request: Request):
    content:  dict[str, Any] = request.json
    nickname: str = content["nickname"]
    password: str = content["password"]
    email:    str = content["email"]

    if not 8 <= len(password) <= 256:
        return text("Password must be between 8 and 256 characters")

    if not validate_email(
            email_address=email,
            check_smtp=False):
        return text("Email is not valid", status=400)

    try:
        user, token = User.create(
            nickname=nickname,
            email=email,
            password=password)
    except DuplicateKeyError as duplicate_error:
        details = duplicate_error.details
        if details is None:
            return text("Internal error", status=400)
        print(details)

        keys = ', '.join(details["keyPattern"])
        error_message = keys + f" {('is','are')[len(details)>1]} taken"
        return text(error_message, status=400)

    return response.redirect(to="/", headers={"set-cookie": urlencode({"token": token})})
