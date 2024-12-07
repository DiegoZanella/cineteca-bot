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
        db_connector.write_to_db(movies)

        return jsonify(movies)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
