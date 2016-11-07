import json
import urllib2
import paho.mqtt.client as mqtt

def on_connect(client, userdata, flags, rc):
    client.subscribe("/test")

def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))

if __name__ == '__main__':
    client = mqtt.Client()
    client.on_connect   = on_connect
    client.on_message   = on_message

    client.connect("localhost", 1884, 60)

    client.loop_forever()
