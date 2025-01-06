import os
import logging
import telebot
import time
from flask import Flask, request, jsonify
from dotenv import load_dotenv
from db_connection import get_movies_for_date, format_date_to_spanish  # Import your database query function
import messages
import requests
from io import BytesIO
import datetime
import threading


# Initialize Flask app and Telegram bot
app = Flask(__name__)

# Configure Logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler()],  # Send logs to stdout for Docker
    force=True  # Override any existing logging configurations
)

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
bot = telebot.TeleBot(TELEGRAM_TOKEN)

# Database credentials (via environment variables)
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_USER = os.getenv("DB_USER", "movie_user")
DB_PASSWORD = os.getenv("DB_PASSWORD", "movie_password")
DB_NAME = os.getenv("DB_NAME", "movies_db")
SCRAPPER_URL = os.getenv("SCRAPPER_URL")
TELEGRAM_CHANNEL_ID = os.getenv("TELEGRAM_CHANNEL_ID")
TELEGRAM_USER_ID = os.getenv("TELEGRAM_USER_ID")

logging.info(f"TELEGRAM_USER_ID: {TELEGRAM_USER_ID}")


@bot.message_handler(commands=["start", "help"])
def send_welcome(message):
    """
    Respond to /start or /help commands.
    """
    bot.reply_to(message, messages.help_message())


@bot.message_handler(commands=["scrape"])
def request_scrapping(message):
    logging.info(str(message.text.split(" ")))
    logging.info(message.text)
    logging.info(message.chat.id)

    # Check if no info was passed in the message
    if len(message.text.split()) == 1:  # the /scrape command will always be in the text
        date = datetime.date.today().strftime("%Y-%m-%d")
    else:
        date = message.text.split()[1]

    try:
        datetime.datetime.strptime(date, "%Y-%m-%d")
    except ValueError:
        bot.reply_to(message, f"Couldn't parse date {date}. "
                              f"Please pass a valid date or leave blank to scrap today's movies")
        return

    logging.info(f"Manually triggered the scraper for date: {date}")
    scrapper_response = requests.get(f"{SCRAPPER_URL}?date={date}")
    logging.info(str(scrapper_response))

    if scrapper_response.status_code == 200:
        logging.info("Scraper completed successfully.")
        bot.reply_to(message, f"Successfully scraped manually movies for date {date}")
    else:
        logging.info(f"Scraper failed: {scrapper_response.text}")
        bot.reply_to(message, f"There was a problem with the scrapping request. Check bot's logs for more info")


@bot.message_handler(commands=["movies"])
def request_movies(message):
    logging.info(message.chat.id)

    if message.chat.id == TELEGRAM_USER_ID:
        bot.reply_to(message, "YOU ARE NOT AUTHORIZED TO CHAT WITH THIS BOT")
        return
    else:
        bot.reply_to(message, "You are authorized to chat with this bot")
    bot.reply_to(message, "This route will someday return some movies")


@app.route('/send_movies', methods=['POST'])
def send_movies_to_channel():
    """
    Query the database and send movie data to the Telegram channel.
    """
    data = request.get_json()
    if not data or "date" not in data:
        return jsonify({"error": "Missing 'date' in request body"}), 400

    date = data["date"]

    try:
        logging.info(f"Querying database for movies on {format_date_to_spanish(date)}...")
        # Query the database for movies on the given date
        movies = get_movies_for_date(date, DB_HOST, DB_USER, DB_PASSWORD, DB_NAME)
        logging.info(f"Number of movies found: {len(movies)}")
        if not movies:
            message = f"No movies found for {date}."
        else:
            message = messages.welcome_message(
                format_date_to_spanish(date)
            )
            bot.send_message(
                chat_id=TELEGRAM_CHANNEL_ID,
                text=message,
                parse_mode="Markdown",
                disable_notification=True
            )
            for movie in movies:
                try:
                    # Download the image in memory
                    response = requests.get(movie["img_link"], timeout=10)
                    response.raise_for_status()  # Raise HTTPError for bad responses (4xx and 5xx)
                    image = BytesIO(response.content)  # Load image into memory
                    image.seek(0)  # Ensure pointer is at the start

                    message = messages.movie_message(movie)
                    bot.send_photo(
                        chat_id=TELEGRAM_CHANNEL_ID,
                        photo=image,  # The link to the movie poster
                        caption=message,
                        parse_mode="Markdown",
                        disable_notification=True  # Disable sound/notification
                    )
                    time.sleep(5)  # Sleep for 5 seconds to avoid rate limiting
                except Exception as e:
                    logging.error(f"Error formatting movie: {e}")
                    logging.error(f"Movie data: {movie}")
                    continue

        # Goodbye message
        bot.send_message(
            chat_id=TELEGRAM_CHANNEL_ID,
            text=messages.goodbye_message(),
            parse_mode="Markdown",
            disable_notification=True
        )
        logging.info(f"Movies sent to channel for date {date}.")

        return jsonify({"message": "Movies sent to Telegram"}), 200

    except Exception as e:
        logging.error(f"Error sending movies: {e}")
        return jsonify({"error": "Internal server error"}), 500


def start_polling():
    """
    Function to start the bot polling
    :return:
    """
    logging.info("Starting bot polling...")
    bot.infinity_polling()


# Start polling for bot commands
if __name__ == "__main__":
    bot_thread = threading.Thread(target=start_polling, daemon=True)
    bot_thread.start()
    logging.info("Bot is running...")

    logging.info(f"Telegram channel ID: {TELEGRAM_CHANNEL_ID}")
    logging.info(f"Database host: {DB_HOST}")
    logging.info(f"Database user: {DB_USER}")

    app.run(host="0.0.0.0", port=5002)
    logging.info("Bot Flask API is running...")

