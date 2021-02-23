import paho.mqtt.client as mqtt
import database

from api import app

USERNAME = "hamid"
PASSWORD = "abcd1234"
DEVICE_NAME = "shellies/shellyem3-68C63AFB5856/"
POWER_CMD = "relay/0/command"
a = 1
B = 4
unacked_sub = []

DB_PATH = 'mydb.db'


def on_connect(client, userdata, flags, rc):
    print("Connection with  returned with result code:" + str(rc))


def on_disconnect(client, userdata, rc):
    print("Disconnection with returned result:" + str(rc))


def on_subscribe(client, userdata, mid, granted_qos):
    unacked_sub.remove(mid)


def on_message(client, userdata, msg):
    Engine = database.Engine(DB_PATH)
    Connection = Engine.connect()
    Connection.create_device("abcd", msg.topic, msg.payload)
    Connection.close()
    print("Received message, topic:" + msg.topic + " payload:" + str(msg.payload))

    # global gv
    # gv = msg.payload
    # if float(msg.payload) > CUT_OFF_VAL:
    # client.publish("shellies/shellyem3-68C63AFB5856/relay/0/command", payload="off")


def initialize_client():
    client = mqtt.Client(client_id="Laptop", clean_session=True, transport="tcp")
    client.username_pw_set(username=USERNAME, password=PASSWORD)
    client.on_connect = on_connect
    client.on_disconnect = on_disconnect
    client.on_message = on_message
    client.on_subscribe = on_subscribe
    return client


def start_mqtt(client, host, port):
    client.connect(host, port, 60)
    client.loop_start()
    return client


def stop_mqtt(client):
    client.loop_stop()
    client.disconnect()


if __name__ == "__main__":
    server = "off"
    client = initialize_client()
    client = start_mqtt(client, "127.0.0.1", 1883)
    client.publish(topic=DEVICE_NAME + POWER_CMD, payload="off")


    # Subscribe to a single topic

    #client.subscribe("shellies/shellyem3-68C63AFB5856/emeter/0/total", 0)
    client.subscribe("shellies/shellyem3-68C63AFB5856/emeter/1/power", 0)
    client.subscribe("shellies/shellyem3-68C63AFB5856/emeter/1/current", 0)
    client.subscribe("shellies/shellyem3-68C63AFB5856/emeter/1/voltage", 0)
    client.subscribe("shellies/shellyem3-68C63AFB5856/emeter/0/total_returned", 0)
    client.subscribe("shellies/shellyem3-68C63AFB5856/emeter/0/returned_energy", 0)
    client.subscribe("shellies/shellyem3-68C63AFB5856/emeter/0/power", 0)
    client.subscribe("shellies/shellyem3-68C63AFB5856/emeter/0/current", 0)
    client.subscribe("shellies/shellyem3-68C63AFB5856/emeter/0/voltage", 0)
    #client.subscribe("shellies/shellyem3-68C63AFB5856/emeter/1/energy", 0)




    while True:
        result, mid = client.subscribe(DEVICE_NAME + "relay/0", 0)
        unacked_sub.append(mid)
        if server is not "on":
            app.run('0.0.0.0')
            server = "on"
        if a is not 1:
            break
    stop_mqtt(client)
