import os
from apscheduler.schedulers.blocking import BlockingScheduler
from main import run_once
from dotenv import load_dotenv
load_dotenv()

interval = int(os.getenv("SCHED_INTERVAL_MIN", "30"))

if _name_ == "_main_":
    sched = BlockingScheduler()
    sched.add_job(run_once, 'interval', minutes=interval, id="scrape_job", max_instances=1)
    print(f"[scheduler] scheduled job every {interval} minutes")
    try:
        sched.start()
    except (KeyboardInterrupt, SystemExit):
        print("Scheduler stopped")