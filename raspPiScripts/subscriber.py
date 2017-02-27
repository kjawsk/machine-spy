import json
import requests
import paho.mqtt.client as mqtt

def post_json_data(json_data):
    headers = {'content-type': 'application/json'}
    r = requests.post(
        'http://localhost:8000/entries',
        data=json_data,
        headers=headers)
    print (r.text)

def on_connect(client, userdata, flags, rc):
    print("Connected with result code: " + str(rc))
    client.subscribe("/test")

def on_message(client, userdata, msg):
    content = msg.payload.decode('utf-8').split("/")

    print(msg.topic + " name: " + str(content[0]) + " value: " +  str(content[1]))

    data = {}
    data['sensor_name'] = content[0]
    data['value'] = content[1]
    json_data = json.dumps(data)
    post_json_data(json_data)

if __name__ == '__main__':
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message

    client.connect("localhost", 1884, 60)

    client.loop_forever()
