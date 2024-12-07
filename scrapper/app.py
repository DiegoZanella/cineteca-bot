from logging.config import listen

from flask import Flask, request, jsonify
import scrapper
import db_connector

app = Flask(__name__)


@app.route('/scraper', methods=['GET'])
def scraper():
    # Retrieve 'date' from query parameters
    date = request.args.get('date')

    if not date:
        return jsonify({"error": "Missing required parameter: date"}), 400

    try:
        # Call the scrapper function with the provided date
        movies = scrapper.start_scrapper(date)
        print("Successful scrapper call")
        print("Writing to DB...")
        db_connector.write_to_db(
            movies,
            host="172.17.0.1",
            user="movie_user",
            password="movie_password",
            database="movies_db"
        )
        print("Write to DB successful")

        return jsonify(movies)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
