from sanic import text,json
from sanic.request import Request

from ..user.user import User

from . import app


@app.get('/users')
async def users(request: Request):
    args = request.query_args
    # didn't test this
    # too lazy to add users to database KEKW
    if "id" in args:
        user = User.get_by_id(args["id"])
        return json(user.dict)
    else:
        # Getting all users from database is a very very bad idea
        # I Suggest to remove this, maybe online users instead ? but in another end-point ?
        # Or users you follow
        raise NotImplementedError

@app.get('/game')
async def game(request: Request):
    return text("Ok")


@app.get('/puzzle')
async def puzzle(request: Request):
    return text("Ok")
