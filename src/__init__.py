import datetime
import json
from bson.objectid import ObjectId
from flask import Flask, jsonify
from flask_cors import CORS, cross_origin

from controllers import app   

if __name__ == '__main__':
	# Run the app
	app.run()



