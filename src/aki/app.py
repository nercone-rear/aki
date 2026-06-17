from kaede import Request, Response, WebSocket, Callback
from typing import Literal, Callable, Awaitable

class Aki(Callback):
    def __init__(self):
        super().__init__()

    async def on_request(self, request: Request) -> Response | Awaitable[Response]:
        ...

    async def on_websocket(self, request: Request, ws: WebSocket):
        ...

    def add_route(self, path: str, *, methods: list[Literal["GET", "HEAD", "POST", "PUT", "DELETE", "CONNECT", "OPTIONS", "TRACE", "PATCH"]] | None = None, callback: Callable[[Request, WebSocket | None], Response]) -> Callable[[Request, WebSocket | None], Response]:
        ...

    def route(self, path: str, *, methods: list[Literal["GET", "HEAD", "POST", "PUT", "DELETE", "CONNECT", "OPTIONS", "TRACE", "PATCH"]] | None = None) -> Callable[[Callable[[Request, WebSocket | None], Response]], Callable[[Request, WebSocket | None], Response]]:
        ...
