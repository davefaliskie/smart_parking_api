from flask import Flask

import models
from resources.lots import lots_api


DEBUG = True
HOST = '0.0.0.0'
PORT = 8000

app = Flask(__name__)
app.register_blueprint(lots_api)

@app.route('/')
def hello_world():
	return "API for collecting reader data for use with Smart Parking app."
	return "Use /api/v1/lots extension to view data."

if __name__ == '__main__':
	models.initialize()
	app.run(debug=DEBUG, host=HOST, port=PORT)
