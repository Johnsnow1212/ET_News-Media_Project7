import requests
from epita_kiran_kumar_ganesan.config import config

def fetch_live_data() -> dict:
    config.validate()
    url = "https://newsapi.org/v2/top-headlines?country=us&pageSize=5"
    headers = {"X-Api-Key": config.api_key}

    resp = requests.get(url, headers=headers, timeout=10)
    resp.raise_for_status()
    data = resp.json()

    articles = data.get("articles", [])
    top_title = articles[0].get("title", "No Title") if articles else "No articles found"
    top_source = articles[0].get("source", {}).get("name", "Unknown") if articles else "Unknown"

    return {
        "status": "LIVE_SUCCESS",
        "total_results": data.get("totalResults", 0),
        "articles_count": len(articles),
        "headline_source": top_source,
        "sample_headline": top_title
    }

if __name__ == "__main__":
    import pprint
    pprint.pprint(fetch_live_data())