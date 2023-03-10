from typing import Optional

import requests

from settings import TIMEOUT_CHECK_PROXY


class CheckProxyRequest:
    def __init__(
        self,
        timeout: int = TIMEOUT_CHECK_PROXY,
        destination_host: str = "",
        destination_host_port: int = 80,
    ) -> None:
        """
        Use public or private proxy to simulate that your access comes from another country
        :param destination_host: Destination host IP or URL
        :param destination_host_port: Port of the application that will be the target
        :param timeout: Maximum waiting time for request return
        """
        self.destination_host: str = destination_host
        self.timeout: int = timeout

        if self.destination_host:
            self.destination_host += str(destination_host_port)

    def _get_session(self, proxy: str, protocol: str) -> requests.Session:
        """
        Construct an HTTP session
        :param proxy: HOST_IP:PORT of the proxy that will be used in the request attempt
        :param protocol: http | sock4 | sock5
        :return: Response from the request
        """
        session: requests.Session = requests.Session()
        if protocol != "http":
            session_host_and_port: str = f"{protocol}://{proxy}"
            session.proxies.update(
                {
                    "http": session_host_and_port,
                    "https": session_host_and_port,
                }
            )
        else:
            session.proxies.update({"https": proxy, "http": proxy})

        return session

    def request(self, proxy: str, protocol: str) -> Optional[requests.Response]:
        """
        :param proxy: HOST_IP:PORT of the proxy that will be used in the request attempt
        :param protocol: http | sock4 | sock5
        :return: Response from the request
        """
        if self.destination_host:
            session = self._get_session(proxy, protocol)
            response: Optional[requests.Response] = session.get(
                self.destination_host, timeout=self.timeout
            )
        else:
            response: Optional[requests.Response] = None
        return response
