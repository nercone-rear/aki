import os
import json
from kaede import Response, Headers
from pathlib import Path

class PlainTextResponse(Response):
    def __init__(self, content: str, *, status_code: int = 200, headers: Headers | None = None, compression: bool = True, file_range: tuple[int, int] | None = None):
        self.body = content.encode()
        self.status_code = status_code
        self.headers = headers or Headers({})
        self.content_type = "text/plain"
        self.compression = compression
        self.minification = False
        self.file_range = file_range

class HTMLResponse(Response):
    def __init__(self, content: str, *, status_code: int = 200, headers: Headers | None = None, compression: bool = True, minification: bool = False, file_range: tuple[int, int] | None = None):
        self.body = content.encode()
        self.status_code = status_code
        self.headers = headers or Headers({})
        self.content_type = "text/html"
        self.compression = compression
        self.minification = minification
        self.file_range = file_range

class JSONResponse(Response):
    def __init__(self, content: list | dict, *, status_code: int = 200, headers: Headers | None = None, compression: bool = True, file_range: tuple[int, int] | None = None):
        self.body = json.dumps(content).encode()
        self.status_code = status_code
        self.headers = headers or Headers({})
        self.content_type = "application/json"
        self.compression = compression
        self.minification = False
        self.file_range = file_range

class FileResponse(Response):
    def __init__(self, path: os.PathLike | Path, *, status_code: int = 200, headers: Headers | None = None, content_type: str | None = None, compression: bool = True, minification: bool = False, file_range: tuple[int, int] | None = None):
        self.body = path
        self.status_code = status_code
        self.headers = headers or Headers({})
        self.content_type = content_type
        self.compression = compression
        self.minification = minification
        self.file_range = file_range

class RedirectResponse(Response):
    def __init__(self, url: str, *, status_code: int = 307, headers: Headers | None = None):
        self.body = None
        self.status_code = status_code
        self.headers = headers or Headers({})
        self.content_type = None
        self.compression = False
        self.minification = False
        self.file_range = None

        self.headers.set("Location", url)
