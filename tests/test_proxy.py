import pytest

from telegram.proxy import SOCKS5Proxy, MTProtoProxy, HTTPProxy, ProxyType


@pytest.mark.parametrize(
    'proxy_class, exp_type',
    [
        (SOCKS5Proxy, ProxyType.SOCKS5),
        (MTProtoProxy, ProxyType.MTPROTO),
        (HTTPProxy, ProxyType.HTTP),
    ],
)
def test_proxy_class_types(proxy_class, exp_type):
    assert proxy_class._type == exp_type


@pytest.mark.parametrize(
    'proxy_type, exp_type_string',
    [
        (ProxyType.SOCKS5, 'proxyTypeSocks5'),
        (ProxyType.MTPROTO, 'proxyTypeMtproto'),
        (ProxyType.HTTP, 'proxyTypeHttp'),
    ],
)
def test_proxy_type_values(proxy_type, exp_type_string):
    assert proxy_type.value == exp_type_string


@pytest.mark.parametrize(
    'proxy_class, exp_type',
    [(SOCKS5Proxy, ProxyType.SOCKS5), (HTTPProxy, ProxyType.HTTP)],
)
def test_proxy_object(proxy_class, exp_type):
    server = '127.0.0.1'
    port = 1122
    username = 'tg'
    password = 'pw'

    proxy = proxy_class(server=server, port=port, username=username, password=password)

    assert proxy.server == server
    assert proxy.port == port

    exp_proxy_object = {
        '@type': exp_type.value,
        'username': username,
        'password': password,
    }

    assert proxy.get_type_object() == exp_proxy_object


def test_mtproto_proxy_object():
    server = 'localserver'
    port = 1122
    secret = 'tg-secret'

    proxy = MTProtoProxy(server=server, port=port, secret=secret)

    assert proxy.server == server
    assert proxy.port == port

    exp_proxy_object = {
        '@type': ProxyType.MTPROTO.value,
        'secret': secret,
    }

    assert proxy.get_type_object() == exp_proxy_object
