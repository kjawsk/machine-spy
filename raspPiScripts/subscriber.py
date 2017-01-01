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

    # req = urllib2.Request('http://localhost:5000/entries')
    # req.add_header('Content-Type', 'application/json')
    # response = urllib2.urlopen(req, json_data)

def on_connect(client, userdata, flags, rc):
    # Connect callback
    print("Connected with result code "+str(rc))
    # Now subscribe
    client.subscribe("/test")

def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload.decode('utf-8')))
    # Prepare JSON Data
    # data = { msg.topic:msg.payload }
    data = dict({'sensor_name':msg.payload.decode('utf-8')})
    json_data = json.dumps(data)
    # Post Sensor Data
    post_json_data(json_data)

def on_subscribe( client, userdata, mid, qos):
    print("Subscribed")

if __name__ == '__main__':
    client = mqtt.Client()
    client.on_connect   = on_connect
    client.on_message   = on_message

    client.connect("localhost", 1884, 60)

    client.loop_forever()
