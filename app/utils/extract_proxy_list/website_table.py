import requests
from bs4 import BeautifulSoup as bs


def extract_proxy_list(url: str) -> list[str]:
    # get the HTTP response and construct soup object
    soup = bs(requests.get(url).content, "html.parser")
    proxies: list[str] = []
    for row in soup.find("table", attrs={"class": "table"}).find_all("tr")[1:]:
        tds = row.find_all("td")
        try:
            ip: str = tds[0].text.strip()
            port: str = tds[1].text.strip()
            host = f"{ip}:{port}"
            proxies.append(host)
        except IndexError:
            continue
    return proxies
