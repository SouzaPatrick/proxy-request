from app.models import ExtractionMethod
from app.utils.extract_proxy_list.search_method import search_method


def test_search_method_website_table_with_contry_code(mocker):
    extraction_method: ExtractionMethod = ExtractionMethod(
        name="",
        url="",
        priority=0,
        method="website_table_with_contry_code",
        protocol_id=1,
    )
    mocker.patch(
        "app.utils.extract_proxy_list.search_method.extract_proxy_list",
        return_value=[
            "192.168.0.1:80",
            "192.168.0.2:80",
            "192.168.0.3:80",
            "192.168.0.4:80",
        ],
    )
    proxies: list[str] = search_method(extract_method=extraction_method)

    assert proxies == [
        "192.168.0.1:80",
        "192.168.0.2:80",
        "192.168.0.3:80",
        "192.168.0.4:80",
    ]


def test_search_method_other(session):
    extraction_method: ExtractionMethod = ExtractionMethod(
        name="",
        url="",
        priority=0,
        method="other",
        protocol_id=1,
    )
    extraction_method.exists(session=session, name="", priority=0)
    proxies: list[str] = search_method(extract_method=extraction_method)
    assert proxies == []
