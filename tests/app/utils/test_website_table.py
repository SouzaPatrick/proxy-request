import pytest

from app.utils.extract_proxy_list.website_table import (
    BaseCascadePipeline,
    WebsiteTablePipeline,
)


class MockResponse:
    def __init__(
        self,
        status_code: int = 200,
        content: bytes = b"Mock content",
        text: str = "Mock text",
        json: dict = {},
    ):
        self.status_code = status_code
        self.content = content
        self.text = text
        self.json = json


@pytest.fixture
def content_file():
    filename: str = "./tests/app/utils/exemple_content.html"
    with open(filename, "rb") as file:
        reader = file.read()
    response = MockResponse(content=reader)
    return response


def test_website_table_pipeline_success(mocker, content_file):
    mocker.patch(
        "app.utils.extract_proxy_list.website_table.requests.get",
        return_value=content_file,
    )

    proxies: list[str] = WebsiteTablePipeline(url="http://test.com").run()

    assert proxies == [
        "103.121.149.69:8080",
        "203.78.235.132:3128",
        "117.54.161.36:9000",
        "20.191.183.93:3129",
        "68.132.18.127:8888",
        "47.88.0.182:443",
        "8.219.176.202:8080",
        "20.191.183.149:3129",
        "162.55.188.41:8020",
        "159.138.130.126:8999",
        "88.99.234.110:2021",
        "46.4.75.218:20000",
        "80.14.219.107:3128",
        "200.105.215.22:33630",
        "200.8.57.8:8080",
        "64.225.4.63:9998",
        "104.248.86.122:443",
        "152.67.10.190:8100",
        "40.119.236.22:80",
        "8.218.239.205:8888",
        "125.17.80.229:8080",
        "42.113.78.207:8080",
        "144.126.141.115:1010",
        "115.144.102.39:10080",
        "185.15.172.212:3128",
        "190.61.88.147:8080",
        "190.2.212.101:999",
        "187.130.139.197:8080",
        "8.219.97.248:80",
        "82.146.48.136:8000",
        "200.25.254.193:54240",
        "13.75.216.118:3128",
        "197.232.48.155:32650",
        "185.73.202.85:80",
        "45.146.167.237:3128",
        "5.189.184.6:80",
        "94.45.223.222:8080",
        "179.96.28.58:80",
        "124.156.87.32:8000",
        "23.236.70.54:45787",
        "20.241.236.196:3128",
        "23.254.209.174:8888",
        "213.230.127.93:3128",
        "51.159.115.233:3128",
        "202.40.177.69:80",
        "167.172.238.15:9992",
        "103.171.183.201:8181",
        "27.199.141.141:1080",
        "64.225.8.132:9979",
        "130.41.109.158:8080",
        "20.191.183.38:3129",
        "65.108.230.239:42899",
        "161.117.227.226:8118",
        "27.147.174.107:8080",
        "90.189.116.152:3128",
        "155.50.243.191:3128",
        "43.249.10.206:45787",
        "20.191.183.123:3129",
        "176.193.12.144:55443",
        "111.225.153.194:8089",
        "195.181.198.178:8118",
        "61.28.238.4:3128",
        "77.233.5.68:55443",
        "103.148.192.83:8089",
        "5.9.139.204:8000",
        "20.191.183.142:3129",
        "198.11.172.137:80",
        "94.130.43.166:8090",
        "146.56.136.237:9090",
        "144.202.100.17:8888",
        "193.141.126.54:82",
        "61.28.233.217:3128",
        "64.225.8.203:9998",
        "68.183.185.62:80",
        "20.122.27.242:80",
        "43.163.229.25:8088",
        "91.226.58.100:3128",
        "103.69.108.78:8191",
        "123.30.154.38:2008",
        "212.46.230.102:6969",
        "161.35.46.209:443",
        "20.191.183.129:3129",
        "116.111.127.9:4001",
        "20.191.183.134:3129",
        "210.148.141.4:8080",
        "198.44.191.43:45787",
        "150.109.12.63:8999",
        "64.20.51.62:8000",
        "202.181.14.23:3128",
        "64.225.4.81:9991",
        "198.59.191.234:8080",
        "103.106.195.41:32650",
        "45.125.217.90:5555",
        "155.50.220.230:3128",
        "173.255.252.54:81",
        "4.16.68.158:443",
        "138.2.117.70:8080",
        "115.96.208.124:8080",
        "78.138.98.115:3128",
        "81.12.44.197:3129",
    ]


def test_base_cascade_pipeline_init():
    assert BaseCascadePipeline().steps == ()
