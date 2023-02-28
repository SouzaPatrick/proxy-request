from app.utils.extract_proxy_list.website_table import extract_proxy_list
from app.check_proxy_request import CheckProxyRequest
from typing import Optional
import requests
from settings import DESTINATION_HOST, TTL_PROXY
from app.db_functions import create_proxies, exist_proxy
from app.models import Proxy
from datetime import datetime

proxies: list[str] = extract_proxy_list(url='https://free-proxy-list.net/')
_proxies = []
for proxy in proxies:
    # Check if the proxy already exists in the database, if it does, ignore the check
    proxy_ip, proxy_port = proxy.split(":")
    if not exist_proxy(ip=proxy_ip, port=int(proxy_port)):
        # Proxy validate
        try:
            proxy_request: Optional[requests.Response] = CheckProxyRequest(destination_host=DESTINATION_HOST).request(host_and_port=proxy)
        except:
            status_check: bool = False
            proxy_request: Optional[requests.Response] = None

        if proxy_request:
            status_check: bool = True
            print(proxy)
            print(proxy_request.status_code)
            print(proxy_request.json())
            print('--------------------------------------------------------')
        else:
            status_check: bool = False

        proxy_ip, proxy_port = proxy.split(':')
        _proxies.append(Proxy(ip=proxy_ip, port=int(proxy_port), status_check=status_check, ttl=TTL_PROXY, last_check=datetime.now()))

create_proxies(proxies=_proxies)
# proxy = '116.98.177.99:10003'
# proxy_request: Optional[requests.Response] = CheckProxyRequest(destination_host=DESTINATION_HOST).request(host_and_port=proxy)
# print(proxy_request.status_code)
# print(proxy_request.json())





