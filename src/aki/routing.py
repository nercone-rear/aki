import re
import inspect
from typing import Callable, Literal
from kaede import Response, WebSocket

from .models import Request
from .responses import PlainTextResponse

PARAM_RE = re.compile(r'\{(\w+)\}')

def compile_path(path: str) -> re.Pattern:
    parts = PARAM_RE.split(path)
    regex_parts = []
    for i, part in enumerate(parts):
        if i % 2 == 0:
            regex_parts.append(re.escape(part))
        else:
            regex_parts.append(f'(?P<{part}>[^/]+)')
    return re.compile(''.join(regex_parts))

class RouteEntry:
    __slots__ = ('path', 'regex', 'methods', 'callback')

    def __init__(self, path: str, methods: frozenset[str] | None, callback: Callable):
        self.path = path
        self.methods = methods
        self.callback = callback
        self.regex = compile_path(path)

class Router:
    def __init__(self):
        self.routes: list[RouteEntry] = []

    def add_route(self, path: str, *, methods: list[Literal["GET", "HEAD", "POST", "PUT", "DELETE", "CONNECT", "OPTIONS", "TRACE", "PATCH"]] | None = None, callback: Callable) -> Callable:
        normalized = frozenset(m.upper() for m in methods) if methods else None
        self.routes.append(RouteEntry(path, normalized, callback))
        return callback

    def route(self, path: str, *, methods: list[Literal["GET", "HEAD", "POST", "PUT", "DELETE", "CONNECT", "OPTIONS", "TRACE", "PATCH"]] | None = None) -> Callable:
        def decorator(func: Callable) -> Callable:
            self.add_route(path, methods=methods, callback=func)
            return func
        return decorator

    async def dispatch(self, request: Request, ws: WebSocket | None) -> Response | None:
        path = request.target.split('?', 1)[0]
        method = request.method.upper()

        allowed: set[str] = set()
        path_matched = False

        for entry in self.routes:
            match = entry.regex.fullmatch(path)
            if match is None:
                continue
            path_matched = True

            if entry.methods is not None and method not in entry.methods:
                allowed.update(entry.methods)
                continue

            result = entry.callback(request, ws, **match.groupdict())
            if inspect.isawaitable(result):
                result = await result
            return result

        if path_matched:
            response = PlainTextResponse("Method Not Allowed", status_code=405)
            response.headers.set("Allow", ", ".join(sorted(allowed)))
            return response

        return PlainTextResponse("Not Found", status_code=404)
