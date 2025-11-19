import os
from scraper.scraper_static import paginate_and_scrape
from scraper.scraper_dynamic import scrape_with_selenium
from db.models import init_db, upsert_items
import logging
from dotenv import load_dotenv

load_dotenv()
LOG = logging.getLogger("scraper_main")
logging.basicConfig(level=logging.INFO)

def run_once():
    LOG.info("Initializing DB (if needed)")
    init_db()
    LOG.info("Starting static scraper (first pass, 1 page for speed)")
    static_items = paginate_and_scrape(max_pages=1)  
    LOG.info(f"Static found {len(static_items)} items (sample)")
    LOG.info("Starting dynamic scraper (selenium)")
    dynamic_items = scrape_with_selenium(max_pages=1)
    LOG.info(f"Dynamic found {len(dynamic_items)} items (sample)")

    
    combined = {}
    for it in static_items + dynamic_items:
        combined[it["external_id"]] = it
    all_items = list(combined.values())
    LOG.info(f"Upserting {len(all_items)} items to DB")
    events = upsert_items(all_items)
    LOG.info(f"Events generated: {events}")

if _name_ == "_main_":
    run_once()