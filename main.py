import json
import os
import logging
from dotenv import load_dotenv


from scraper.scraper_static import paginate_and_scrape
from scraper.scraper_dynamic import scrape_with_selenium
from db.models import init_db, upsert_items


load_dotenv()


os.makedirs("logs", exist_ok=True)
os.makedirs("data", exist_ok=True)


logging.basicConfig(
    filename="logs/scraper.log",
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    encoding="utf-8"
)

LOG = logging.getLogger("scraper")


def run_once():
    LOG.info("===== Scraper Execution Started =====")

    LOG.info("Initializing DB (if needed)")
    init_db()


    LOG.info("Starting static scraper (first pass, 1 page)")
    try:
        static_items = paginate_and_scrape(max_pages=1)
        LOG.info(f"Static scraper fetched {len(static_items)} items")
    except Exception as e:
        LOG.error(f"Static scraper error: {e}")
        static_items = []


    LOG.info("Starting dynamic scraper (selenium)")
    try:
        dynamic_items = scrape_with_selenium(max_pages=1)
        LOG.info(f"Dynamic scraper fetched {len(dynamic_items)} items")
    except Exception as e:
        LOG.error(f"Selenium scraper error: {e}")
        dynamic_items = []


    combined = {}
    for it in static_items + dynamic_items:
        combined[it["external_id"]] = it

    all_items = list(combined.values())
    LOG.info(f"Combined items ready: {len(all_items)}")


    LOG.info(f"Upserting {len(all_items)} items to DB")
    try:
        events = upsert_items(all_items)
        LOG.info(f"{len(events)} events generated")
    except Exception as e:
        LOG.error(f"Database error during upsert: {e}")
        events = []


    try:
        os.makedirs("data/files", exist_ok=True)

        downloaded_files = []

 
        for item in all_items:
            files = item.get("files", [])

            saved_paths = []
            for f_url in files:
                try:
                    import requests
                    fname = f_url.split("/")[-1]
                    local_path = os.path.join("data/files", fname)

                    resp = requests.get(f_url, timeout=15)
                    resp.raise_for_status()

                    with open(local_path, "wb") as f:
                        f.write(resp.content)

                    saved_paths.append(local_path)

                except Exception as fe:
                    LOG.error(f"Failed to download file {f_url}: {fe}")

    
            item["files"] = saved_paths
            downloaded_files.extend(saved_paths)


        with open("data/results.json", "w", encoding="utf-8") as f:
            json.dump(all_items, f, indent=2, ensure_ascii=False)

        with open("data/events.json", "w", encoding="utf-8") as f:
            json.dump(events, f, indent=2, ensure_ascii=False)

        with open("data/files.json", "w", encoding="utf-8") as f:
            json.dump(downloaded_files, f, indent=2, ensure_ascii=False)

        LOG.info("Files, results.json, events.json and files.json saved.")
    except Exception as e:
        LOG.error(f"Error writing JSON files or downloading attachments: {e}")


    LOG.info("===== Scraper Execution Finished =====\n")


if __name__ == "__main__":
    run_once()
