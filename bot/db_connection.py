import mysql.connector
from datetime import datetime
import locale
from dotenv import load_dotenv
import os
from babel.dates import format_date
from datetime import datetime
import mariadb


DB_HOST = os.getenv("DB_HOST")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_DATABASE = os.getenv("DB_DATABASE")


def format_date_to_spanish(date):
    # Set the locale to Spanish (for correct day/month names)
    locale.setlocale(locale.LC_TIME, "es_ES")

    # Convert the input date (YYYY-MM-DD) to the localized format
    input_date = datetime.strptime(date, "%Y-%m-%d")
    localized_date = input_date.strftime("%A %d de %B de %Y")  # E.g., "domingo 08 de diciembre de 2024"

    # print(localized_date)
    # localized_date = format_date_to_spanish(date)

    return localized_date


def get_movies_for_date(date, db_host, db_user, db_password, db_name):
    """
    Queries the database for all movies with a screening time on the given date.
    Args:
        date (str): The date to filter screenings (format: YYYY-MM-DD).
        db_host (str): The database host.
        db_user (str): The database user.
        db_password (str): The database password.
        db_name (str): The database name.
    Returns:
        list[dict]: A list of dictionaries containing movie details and screening times.
    """
    try:
        localized_date = format_date_to_spanish(date)

        # Connect to the database
        connection = mariadb.connect(
            host=db_host,
            user=db_user,
            password=db_password,
            database=db_name
        )
        cursor = connection.cursor(dictionary=True)

        # Query for movies with a screening time on the given localized date
        query = """
            SELECT DISTINCT movies.film_id, movies.title, movies.director, movies.duration,
                            movies.img_link, movies.description, times.day, times.time
            FROM movies
            INNER JOIN times ON movies.film_id = times.film_id
            WHERE times.day = %s;
        """

        cursor.execute(query, (localized_date,))

        # Organize the data into a dictionary grouped by movie
        movies = {}
        for row in cursor.fetchall():
            film_id = row["film_id"]
            if film_id not in movies:
                # Add new movie entry
                movies[film_id] = {
                    "movie_id": film_id,
                    "title": row["title"],
                    "director": row["director"],
                    "img_link": row["img_link"],
                    "duration": row["duration"],
                    "description": row["description"],
                    "screening_times": []
                }
            # Add screening time as a tuple (day, hour)
            movies[film_id]["screening_times"].append((row["day"], row["time"]))

        # Return the list of movies
        return list(movies.values())

    except mysql.connector.Error as err:
        print(f"Database error: {err}")
        return []
    except Exception as e:
        print(f"Error: {e}")
        return []
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'connection' in locals():
            connection.close()
