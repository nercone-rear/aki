import ipaddress
from kaede import Request as KaedeRequest, Headers, H2Info, H3Info, TLSInfo
from typing import Any, Literal, MutableMapping

Scope = MutableMapping[str, Any]

class Request(KaedeRequest):
    def __init__(self, method: Literal["GET", "HEAD", "POST", "PUT", "DELETE", "CONNECT", "OPTIONS", "TRACE", "PATCH"], target: str, client: tuple[ipaddress.IPv4Address | ipaddress.IPv6Address, int] | None = None, scheme: Literal["http", "https"] = "http", secure: bool = False, protocol: Literal["HTTP/1.1", "HTTP/2.0", "HTTP/3.0"] = "HTTP/1.1", headers: Headers | None = None, body: bytes | None = None, h2: H2Info | None = None, h3: H3Info | None = None, tls: TLSInfo | None = None, scope: Scope | None = None):
        super().__init__(method=method, target=target, client=client or (ipaddress.IPv4Address("0.0.0.0"), 0), scheme=scheme, secure=secure, protocol=protocol, headers=headers or Headers(), body=body, h2=h2, h3=h3, tls=tls)
        self.scope: Scope = scope if scope is not None else {}

    @classmethod
    def from_kaede(cls, request: KaedeRequest) -> 'Request':
        return cls(method=request.method, target=request.target, client=request.client, scheme=request.scheme, secure=request.secure, protocol=request.protocol, headers=request.headers, body=request.body, h2=request.h2, h3=request.h3, tls=request.tls)
