
# mport paho-mqtt Client class:
import paho.mqtt.client as mqtt
import time
from flask import Flask


gv = ''
CUT_OFF_VAL = 40
unacked_sub = [] # a list for unacknowledged subscription

# Define the callback to handle CONNACK from the broker, if the connection created normal, the value of rc is 0
def on_connect(client, userdata, flags, rc):
    print("Connection returned with result code:" + str(rc))


# Define the callback to hande publish from broker, here we simply print out the topic and payload of the received message
def on_message(client, userdata, msg):
    print("Received message, topic:" + msg.topic + "payload:" + str(msg.payload))
    global gv
    gv = msg.payload


    if float(msg.payload) > CUT_OFF_VAL:
        client.publish("shellies/shellyem3-68C63AFB5856/relay/0/command", payload="off")



# Callback handles disconnection, print the rc value
def on_disconnect(client, userdata, rc):
    print("Disconnection returned result:"+ str(rc))

# Remove the message id from the list for unacknowledged subscription
def on_subscribe(client, userdata, mid, granted_qos):
    unacked_sub.remove(mid)


# Create an instance of `Client`
client = mqtt.Client()
client.username_pw_set(username="hamid", password="abcd1234")
client.on_connect = on_connect
client.on_disconnect= on_disconnect
client.on_message = on_message
client.on_subscribe = on_subscribe

# Connect to broker
# connect() is blocking, it returns when the connection is successful or failed. If you want client connects in a non-blocking way, you may use connect_async() instead
client.connect("127.0.0.1", 1883, 60)

client.loop_start()

# Subscribe to a single topic
#result, mid = client.subscribe("shellies/shellyem3-68C63AFB5856/emeter/0/total", 0)
result, mid = client.subscribe("shellies/shellyem3-68C63AFB5856/emeter/0/power", 0)
#result, mid = client.subscribe("shellies/shellyem3-68C63AFB5856/emeter/1/current", 0)
#result, mid = client.subscribe("shellies/shellyem3-68C63AFB5856/emeter/0/total_returned", 0)
#result, mid = client.subscribe("shellies/shellyem3-68C63AFB5856/emeter/0/returned_energy", 0)
result, mid = client.subscribe("shellies/shellyem3-68C63AFB5856/emeter/1/power", 0)
#result, mid = client.subscribe("shellies/shellyem3-68C63AFB5856/emeter/0/current", 0)
#result, mid = client.subscribe("shellies/shellyem3-68C63AFB5856/emeter/1/energy", 0)
#unacked_sub.append(mid)
# Subscribe to multiple topics
result, mid = client.subscribe([("temperature", 0), ("humidity", 0)])
unacked_sub.append(mid)

while len(unacked_sub) != 0:
   time.sleep(0)

client.publish("hellos1234", payload = "Hello world!")
client.publish("smartmeter", payload = "Hello grid!")
client.publish("temperature", payload = "24.0")
client.publish("humidity", payload = "65%")
client.publish("hello", payload = "Hello world!")
client.publish("shellies/shellyem3-68C63AFB5856/relay/0/command", payload = "on")


#app = Flask(__name__)
#@app.route('/')
#def index():
#    return gv

#if __name__ == "__main__" :
#     app.run()
# Disconnection
time.sleep(4294967) # wait till all messages are processed (49 days)
client.loop_stop()
client.disconnect()

