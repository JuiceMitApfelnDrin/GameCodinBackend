from sanic import text,json
from sanic.request import Request

from ..user.user import User
from bson.objectid import ObjectId

from . import app

# XXX: maybe we should seperate this to differnt modules
# And put them in their respective folders for exemple users/user_routing.py etc..
# Or just put them here, and import all of them to here

@app.get('/users')
async def users(request: Request):
    args = request.args
    if "id" not in args:
        return text("No user_id was provided :(")

    user = User.get_by_id(ObjectId(args["id"][0]))
    if user is None:
        return text("Can't find user :(")
    return json(user.dict)

@app.get('/game')
async def game(request: Request):
    return text("Ok")


@app.get('/puzzle')
async def puzzle(request: Request):
    return text("Ok")
