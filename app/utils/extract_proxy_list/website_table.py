import requests
from bs4 import BeautifulSoup as bs
from bs4.element import Tag


class BaseCascadePipeline:
    def __init__(self) -> None:
        self.steps = ()

    def run(self):
        result: any = self.steps[0]()
        for step in self.steps[1::]:
            result: any = step(result)

        return result


class WebsiteTablePipeline(BaseCascadePipeline):
    def __init__(self, url: str) -> None:
        self.url = url
        self.steps = (
            self.download,
            self.html_parser,
            self.sanitize,
        )

    def download(self) -> requests.Response:
        response = requests.get(self.url)
        return response

    @staticmethod
    def html_parser(response: requests.Response) -> list[Tag]:
        soup = bs(response.content, "html.parser")

        soup_find: list[Tag] = soup.find("table", attrs={"class": "table"}).find_all(
            "tr"
        )[1:]

        return soup_find

    @staticmethod
    def sanitize(soup_find: list[Tag]) -> list[str]:
        proxies: list[str] = []
        for row in soup_find:
            tds = row.find_all("td")
            ip: str = tds[0].text.strip()
            port: str = tds[1].text.strip()
            host = f"{ip}:{port}"
            proxies.append(host)
        return proxies
