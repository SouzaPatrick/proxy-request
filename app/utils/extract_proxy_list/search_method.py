from app.models import ExtractionMethod
from app.utils.extract_proxy_list.website_table import extract_proxy_list


def search_method(extract_method: ExtractionMethod):
    match extract_method.method:
        case "website_table_with_contry_code":
            proxies: list[str] = extract_proxy_list(url=extract_method.url)
        case other:
            proxies: list[str] = []
            print("Invalid method")

    return proxies
