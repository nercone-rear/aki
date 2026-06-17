from kaede import Request as KaedeRequest, Response, WebSocket, Callback
from typing import Literal, Callable

from .models import Request
from .routing import Router

class Aki(Callback):
    def __init__(self):
        super().__init__()
        self.router = Router()

    async def on_request(self, request: KaedeRequest) -> Response:
        return await self.router.dispatch(Request.from_kaede(request), ws=None)

    async def on_websocket(self, request: KaedeRequest, ws: WebSocket):
        await self.router.dispatch(Request.from_kaede(request), ws=ws)

    def add_route(self, path: str, *, methods: list[Literal["GET", "HEAD", "POST", "PUT", "DELETE", "CONNECT", "OPTIONS", "TRACE", "PATCH"]] | None = None, callback: Callable) -> Callable:
        return self.router.add_route(path, methods=methods, callback=callback)

    def route(self, path: str, *, methods: list[Literal["GET", "HEAD", "POST", "PUT", "DELETE", "CONNECT", "OPTIONS", "TRACE", "PATCH"]] | None = None) -> Callable:
        return self.router.route(path, methods=methods)
