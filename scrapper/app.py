from logging.config import listen
import os
from flask import Flask, request, jsonify
import scrapper
import db_connector

db_host = os.getenv("DB_HOST")
db_user = os.getenv("DB_USER")
db_password = os.getenv("DB_PASSWORD")
db_database = os.getenv("DB_DATABASE")

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
            host=db_host,
            user=db_user,
            password=db_password,
            database=db_database
        )
        print("Write to DB successful")

        return jsonify([movie.json_serialize() for movie in movies])
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
