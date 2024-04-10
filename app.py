from flask import Flask, request
from flask_cors import CORS  # pip install Flask-Cors
from sentiment_files.ChromeSentimentMethods import sentiment_product_main

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})


@app.route('/sentiment', methods=['POST', 'GET'])
def sentiment_product_data():
    return sentiment_product_main()


if __name__ == '__main__':
    app.run()
