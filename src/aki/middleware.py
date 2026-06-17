from typing import Callable, Awaitable
from kaede import Response

from .models import Request

Middleware = Callable[[Request, Callable[[Request], Awaitable[Response]]], Awaitable[Response]]
