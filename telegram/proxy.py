from typing import Dict
from enum import Enum


class ProxyType(Enum):
    MTPROTO = 'proxyTypeMtproto'
    SOCKS5 = 'proxyTypeSocks5'
    HTTP = 'proxyTypeHttp'


class BaseProxy:
    server = 'localserver'
    port = 1234
    _type: ProxyType = ProxyType.MTPROTO
    username = ''
    password = ''
    secret = ''

    def get_type_object(self) -> Dict[str, str]:
        data = {
            '@type': self._type.value,
        }
        if self.username:
            data['username'] = self.username
        if self.password:
            data['password'] = self.password
        if self.secret:
            data['secret'] = self.secret

        return data


class BaseUsernamePasswordProxy(BaseProxy):
    def __init__(
        self, server: str, port: int, username: str, password: str,
    ):
        self.server = server
        self.port = port
        self.username = username
        self.password = password


class SOCKS5Proxy(BaseUsernamePasswordProxy):
    _type = ProxyType.SOCKS5


class HTTPProxy(BaseUsernamePasswordProxy):
    _type = ProxyType.HTTP


class MTProtoProxy(BaseProxy):
    _type = ProxyType.MTPROTO

    def __init__(
        self, server: str, port: int, secret: str,
    ):
        self.server = server
        self.port = port
        self.secret = secret
