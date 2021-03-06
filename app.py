from flask import Flask

import models
from resources.spaces import spaces_api


DEBUG = True
HOST = '0.0.0.0'
PORT = 8000

app = Flask(__name__)
app.register_blueprint(spaces_api)

@app.route('/')
def hello_world():
	return "API for collecting reader data for use with Smart Parking app. \n Use /api/v1/spaces extension to view data."

if __name__ == '__main__':
	models.initialize()
	app.run(debug=DEBUG, host=HOST, port=PORT)
