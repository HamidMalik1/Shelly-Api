from flask import Flask, jsonify, Response
from flask_cors import CORS
import database
import json

DB_PATH = 'mydb.db'

app = Flask(__name__)
CORS(app)


def create_error_response(status_code, code=0, message=None):
    response = jsonify(code=code, message=message, data=None)
    response.status_code = status_code
    return response


def bad_request_response(message=None):
    return create_error_response(400, message=message)


@app.errorhandler(404)
def resource_not_found(error):
    return create_error_response(404, message="This resource url does not exist")


@app.errorhandler(400)
def invalid_parameter(error):
    return create_error_response(400, message="Invalid or missing parameters")


@app.errorhandler(500)
def unknown_error(error):
    return create_error_response(
        500, message="The system has failed. Please, contact the administrator"
    )


@app.route("/")
def hello_world():
    return jsonify({"message": "Hello World!"})


@app.route("/devices/<device_name>", methods=["GET"])
def get_devices(device_name):
    Engine = database.Engine(DB_PATH)
    Connection = Engine.connect()
    device_db = Connection.get_device(device_name)
    # print(device_db)
    Connection.close()
    if not device_db:
        return create_error_response(404, "Device not found", "There is no a member with id %dsS" % device_name)
    for device in device_db:
        print(device)
    return jsonify({"code": 200, "message": "Success", "data": device_db})

    #return Response(, 200, mimetype=COLLECTIONJSON + ";" + GROUP_PROFILE)

