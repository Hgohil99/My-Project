from apscheduler.schedulers.background import BackgroundScheduler
from app.fetcher import fetch_stock_metrics, save_metrics_to_csv
from app.config import CONFIG
import time
import os

def delete_old_logs(days_to_keep=2):
    folder = r"D:\Hardik\Coding\My Project\sm_app_v1\StockLogs"
    cutoff = time.time() - days_to_keep * 86400
    deleted = []
    for file in os.listdir(folder):
        path = os.path.join(folder, file)
        if os.path.isfile(path) and os.path.getmtime(path) < cutoff:
            os.remove(path)
            deleted.append(file)
    if deleted:
        print(f" Deleted {len(deleted)} old log(s): {deleted}")
    else:
        print(" No old logs to delete.")

def scheduled_task():
    results = []
    for symbol in CONFIG["stocks_to_track"]:
        data = fetch_stock_metrics(symbol)
        results.append(data)
    save_metrics_to_csv(results)
    print("Data has been stored")
    delete_old_logs(days_to_keep=2)

if __name__ == "__main__":
    scheduler = BackgroundScheduler()
    scheduler.add_job(scheduled_task, trigger="cron", day_of_week="mon-fri", hour=9, minute=0)
    scheduler.add_job(scheduled_task, trigger="cron", day_of_week="mon-fri", hour=15, minute=30)
    scheduler.start()
    print("📅 Scheduler active: Mon–Fri at 9:00 AM & 3:30 PM")

    try:
        while True:
            time.sleep(60)
    except KeyboardInterrupt:
        scheduler.shutdown()
        print("Scheduler stopped")
    