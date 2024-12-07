import mysql.connector


def connect_to_db(host, user, password, database):
    """
        Establishes a connection to the MariaDB database.
        Returns:
            connection: A MySQL connection object
        """
    try:
        connection = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database,
            charset="utf8mb4",
            collation="utf8mb4_general_ci"
        )
        return connection
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        raise


def write_to_db(movies, host, user, password, database):
    """
    Writes the scraped movie data to the MariaDB database.
    Args:
        movies (list): A list of Movie objects
        host (str): The database host
        user (str): The database user
        password (str): The database password
        database (str): The database name
    """
    connection = connect_to_db(host, user, password, database)
    cursor = connection.cursor()

    try:
        for movie in movies:
            # Insert movie data into the `movies` table
            movie_query = """
                INSERT INTO movies (film_id, title, duration, director, description, img_link)
                VALUES (%s, %s, %s, %s, %s, %s)
                ON DUPLICATE KEY UPDATE
                    title = VALUES(title),
                    duration = VALUES(duration),
                    director = VALUES(director),
                    description = VALUES(description),
                    img_link = VALUES(img_link);
            """
            movie_data = (
                movie.film_id,
                movie.title,
                movie.duration,
                movie.director,
                movie.description,
                movie.img_link
            )
            cursor.execute(movie_query, movie_data)

            # Insert movie times into the `times` table
            for day, time in movie.times:
                time_query = """
                    INSERT INTO times (film_id, day, time)
                    VALUES (%s, %s, %s)
                    ON DUPLICATE KEY UPDATE
                        day = VALUES(day),
                        time = VALUES(time);
                """
                time_data = (movie.film_id, day, time)
                cursor.execute(time_query, time_data)

        # Commit the transaction
        connection.commit()
        print("Data successfully written to the database.")
    except mysql.connector.Error as err:
        print(f"Database Error: {err}")
        connection.rollback()
        raise
    finally:
        cursor.close()
        connection.close()
