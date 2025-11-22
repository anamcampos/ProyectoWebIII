import json
import os

def run_once():
    LOG.info("Initializing DB (if needed)")
    init_db()

    LOG.info("Starting static scraper (first pass, 1 page)")
    static_items = paginate_and_scrape(max_pages=1)

    LOG.info("Starting dynamic scraper (selenium)")
    dynamic_items = scrape_with_selenium(max_pages=1)

    combined = {}
    for it in static_items + dynamic_items:
        combined[it["external_id"]] = it
    all_items = list(combined.values())

    LOG.info(f"Upserting {len(all_items)} items to DB")
    events = upsert_items(all_items)

    os.makedirs("data", exist_ok=True)

    with open("data/results.json", "w", encoding="utf-8") as f:
        json.dump(all_items, f, indent=2, ensure_ascii=False)

    with open("data/events.json", "w", encoding="utf-8") as f:
        json.dump(events, f, indent=2, ensure_ascii=False)

    files_list = []  
    with open("data/files.json", "w", encoding="utf-8") as f:
        json.dump(files_list, f, indent=2, ensure_ascii=False)

    LOG.info("JSON files updated in /data/")
