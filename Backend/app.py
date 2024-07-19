from flask import Flask, jsonify, request
from flask_cors import CORS
import logging

app = Flask(__name__)
CORS(app)  # Abilita CORS per permettere al frontend di fare richieste al backend

# Configura il logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

@app.route('/')
def home():
    return jsonify(message="Welcome to the Flask API")

@app.route('/playlist', methods=['GET'])
def get_playlist():
    playlist = {
        "name": "Cooling Vibes: Chill & Refresh",
        "description": "Brani freschi e rilassanti per affrontare il caldo estivo.",
        "public": True,
        "tracks": [
            'Summertime Ella Fitzgerald & Louis Armstrong',
            'Under the Boardwalk The Drifters',
            'Cool Change Little River Band',
            'Here Comes the Sun The Beatles',
            'Island in the Sun Weezer',
            'Summer Breeze Seals & Crofts',
            'Walking on Sunshine Katrina and the Waves',
            'Heat Wave Martha Reeves & The Vandellas',
            'Summer in the City The Lovin\' Spoonful',
            'Sunshine Reggae Laid Back',
            'Kokomo The Beach Boys',
            'Sunny Boney M.',
            'Groovin\' The Young Rascals',
            'In the Summertime Mungo Jerry',
            'Hot Fun in the Summertime Sly & The Family Stone',
            'Tequila Sunrise Eagles',
            'California Dreamin\' The Mamas & The Papas',
            'Good Vibrations The Beach Boys',
            'Lovely Day Bill Withers',
            'Cruel Summer Bananarama'
        ]
    }
    return jsonify(playlist)

if __name__ == '__main__':
    app.run(debug=True)
