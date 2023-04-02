from app.utils.extract_proxy_list.website_table import WebsiteTablePipeline


def search_method(method: str, url=str) -> list[str]:
    match method:
        case "website_table_with_contry_code":
            proxies: list[str] = WebsiteTablePipeline(url=url).run()
        case other:
            proxies: list[str] = []
            print(f"Invalid method: {other}")

    return proxies
