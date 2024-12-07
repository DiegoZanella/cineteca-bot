from apscheduler.schedulers.blocking import BlockingScheduler
import requests
import datetime

SCRAPER_URL = "http://172.17.0.1:5001/scraper"
BOT_URL = "http://bot_service_container:5000/send"


def run_daily_task():
    # Step 1: Trigger the scraper to scrape today's data
    today = datetime.date.today().strftime("%Y-%m-%d")
    print(f"Triggering the scraper for date: {today}")
    scraper_response = requests.get(f"{SCRAPER_URL}?date={today}")

    if scraper_response.status_code == 200:
        print("Scraper completed successfully.")
        # Step 2: Notify the bot to send the data
        #bot_response = requests.post(BOT_URL)
        #if bot_response.status_code == 200:
        #    print("Bot sent the data successfully.")
        #else:
        #    print(f"Bot failed: {bot_response.text}")
    else:
        print(f"Scraper failed: {scraper_response.text}")


# Configure the scheduler
scheduler = BlockingScheduler()
scheduler.add_job(run_daily_task, 'cron', hour=7, minute=0)  # Run at 7:00 AM

if __name__ == "__main__":
    print("Starting scheduler...")
    scheduler.start()
