import pytest

from app.utils.extract_proxy_list.search_method import search_method


@pytest.mark.parametrize(
    "_method,_expected_result",
    (
        ("website_table_with_contry_code", ["0.0.0.0:80", "1.1.1.1:8080"]),
        ("other_method", []),
    ),
)
def test_search_method(_method, _expected_result, mocker):
    mocker.patch(
        "app.utils.extract_proxy_list.search_method.WebsiteTablePipeline.run",
        return_value=_expected_result,
    )
    proxies: list[str] = search_method(method=_method, url="http://teste.com")
    assert proxies == _expected_result
