from kaede import Request as KaedeRequest, Response, WebSocket, Callback
from typing import Literal, Callable

from .models import Request
from .routing import Router
from .middleware import Middleware

def wrap_middleware(middleware: Middleware, next_handler: Callable) -> Callable:
    async def handler(request: Request) -> Response:
        return await middleware(request, next_handler)
    return handler

class Aki(Callback):
    def __init__(self):
        super().__init__()
        self.router = Router()
        self.middlewares: list[Middleware] = []

    def add_middleware(self, middleware: Middleware) -> None:
        self.middlewares.append(middleware)

    def middleware(self, middleware: Middleware) -> Middleware:
        self.add_middleware(middleware)
        return middleware

    async def on_request(self, request: KaedeRequest) -> Response:
        aki_request = Request.from_kaede(request)

        async def endpoint(request: Request) -> Response:
            return await self.router.dispatch(request, ws=None)

        handler = endpoint
        for mw in reversed(self.middlewares):
            handler = wrap_middleware(mw, handler)

        return await handler(aki_request)

    async def on_websocket(self, request: KaedeRequest, ws: WebSocket):
        await self.router.dispatch(Request.from_kaede(request), ws=ws)

    def add_route(self, path: str, *, methods: list[Literal["GET", "HEAD", "POST", "PUT", "DELETE", "CONNECT", "OPTIONS", "TRACE", "PATCH"]] | None = None, callback: Callable) -> Callable:
        return self.router.add_route(path, methods=methods, callback=callback)

    def route(self, path: str, *, methods: list[Literal["GET", "HEAD", "POST", "PUT", "DELETE", "CONNECT", "OPTIONS", "TRACE", "PATCH"]] | None = None) -> Callable:
        return self.router.route(path, methods=methods)
