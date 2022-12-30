from typing import Final, Iterable

from ...environment_variables import load_dotenv

frontend_url: Final = load_dotenv()['FRONTEND_URL']

def _add_cors_headers(response, methods: Iterable[str]) -> None:
    allow_methods = list(set(methods))
    if "OPTIONS" not in allow_methods:
        allow_methods.append("OPTIONS")
    headers = {
        "Access-Control-Allow-Methods": ",".join(allow_methods),
        "Access-Control-Allow-Origin": frontend_url,
        "Access-Control-Allow-Credentials": "true",
        "Access-Control-Allow-Headers": "*",
    }
    response.headers.extend(headers)


def add_cors_headers(request, response):
    if request.method != "OPTIONS":
        methods = [method for method in request.route.methods]
        _add_cors_headers(response, methods)
