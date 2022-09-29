from sanic import text

from . import app


@app.get('/users')
async def users(request):
    return text("Ok")


@app.get('/game')
async def game(request):
    return text("Ok")


@app.get('/puzzle')
async def puzzle(request):
    return text("Ok")
