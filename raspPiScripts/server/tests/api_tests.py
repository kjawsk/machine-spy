import time
import paho.mqtt.client as mqtt
from time import sleep

client = mqtt.Client()
client.connect("192.168.0.103",1884,60)
before = time.time()
for x in range(0, 190):
    client.publish("/test", "ESP8266-1351177/190");
    sleep(0.005)
after = time.time()
client.disconnect();
print("time elapsed: %s" % str(after-before))
