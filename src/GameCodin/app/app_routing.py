from sanic import text

from . import app

@app.get('/users')
async def handler(request):
    return text("Ok")