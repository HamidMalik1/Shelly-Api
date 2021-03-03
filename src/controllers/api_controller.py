from flask import Flask, jsonify, Response
from flask_cors import CORS
import json
from controllers import bad_request_response, app
from model import database

DB_PATH = 'model/mydb.db'

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

