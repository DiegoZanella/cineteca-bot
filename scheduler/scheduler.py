from apscheduler.schedulers.blocking import BlockingScheduler
import requests
import datetime
import os
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,  # Log level
    format="%(asctime)s - %(levelname)s - %(message)s",  # Log format
    handlers=[
        logging.StreamHandler()  # Output logs to stdout for Docker
    ]
)

# SCRAPER_URL = "http://172.17.0.1:5001/scraper"
# BOT_URL = "http://bot_service_container:5000/send"

SCRAPER_URL = os.getenv("SCRAPER_URL")
BOT_URL = os.getenv("BOT_URL")
RUN_HOUR = int(os.getenv("RUN_HOUR", 7))  # Default to 7 AM
RUN_MINUTE = int(os.getenv("RUN_MINUTE", 0))  # Default to 0 minutes
logging.info(RUN_HOUR)
logging.info(RUN_MINUTE)


def run_daily_task():
    # Step 1: Trigger the scraper to scrape today's data
    today = datetime.date.today().strftime("%Y-%m-%d")
    logging.info(f"Triggering the scraper for date: {today}")
    scraper_response = requests.get(f"{SCRAPER_URL}?date={today}")

    if scraper_response.status_code == 200:
        logging.info("Scraper completed successfully.")
        # Step 2: Notify the bot to send the data
        #bot_response = requests.post(BOT_URL)
        #if bot_response.status_code == 200:
        #    print("Bot sent the data successfully.")
        #else:
        #    print(f"Bot failed: {bot_response.text}")
    else:
        logging.info(f"Scraper failed: {scraper_response.text}")


# Configure the scheduler
scheduler = BlockingScheduler()
scheduler.add_job(run_daily_task, 'cron', hour=RUN_HOUR, minute=RUN_MINUTE)  # Run at 7:00 AM

if __name__ == "__main__":
    logging.info("Starting scheduler...")
    scheduler.start()
