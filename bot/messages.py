def welcome_message(date):
    message = (
        f"¡Hola! 🍿🎥\n\n"
        f"Estos son los horarios de películas para el día de hoy, {date}:\n\n"
    )

    return message


def movie_message(movie):
    message = (
        f"🎬 *{movie['title']}*\n"
        f"📅 Horarios: {', '.join([f'{d} {t}' for d, t in movie['screening_times']])}\n"
        f"🕒 Duración: {movie['duration']} \n"
        f"🎥 Director: {movie['director']}\n"
        f"📖 Descripción: {movie['description']}\n\n"
    )

    return message


def goodbye_message():
    message = "Esta fue la cartelera para el día de hoy. ¡Hasta mañana! 🍿🎥"

    return message


def help_message():
    message = ("Available routes for this bot:"
               "\\scrape manually requests a scrapping (pass date in format %Y-%m-%d or leave blank to use today's date"
               "\\movies manually request movies (under construction)")

    return message
