import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import os

SITE_URL = os.getenv("SITE_URL", "https://books.toscrape.com")

def scrape_static_page(url):
    """
    Scrape a single page of books.toscrape.com and return list of item dicts.
    """
    resp = requests.get(url, timeout=15)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "html.parser")
    results = []
    for article in soup.select("article.product_pod"):
        a = article.select_one("h3 a")
        title = a["title"].strip()
        relative = a["href"]
        book_url = urljoin(url, relative)
        # price
        price_tag = article.select_one(".price_color")
        price = price_tag.get_text(strip=True) if price_tag else None
        # build external id from url
        external_id = book_url.split("/")[-2] if "/" in book_url else book_url
        results.append({
            "external_id": external_id,
            "title": title,
            "price": price,
            "url": book_url
        })
    return results

def paginate_and_scrape(start_url=None, max_pages=None):
    """
    Paginate site and collect items from each page until no next or max_pages reached.
    """
    if start_url is None:
        start_url = SITE_URL
    page = 1
    url = start_url
    all_items = []
    while url:
        print(f"[scraper_static] scraping page {page}: {url}")
        items = scrape_static_page(url)
        all_items.extend(items)
        # next page
        resp = requests.get(url, timeout=15)
        soup = BeautifulSoup(resp.text, "html.parser")
        next_li = soup.select_one("li.next a")
        if not next_li:
            break
        next_href = next_li["href"]
        url = url.rsplit("/", 1)[0] + "/" + next_href if "catalogue" in url else urljoin(url, next_href)
        page += 1
        if max_pages and page > max_pages:
            break
    return all_items
