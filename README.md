# machineSpy

This project is a home automation system. Now it allows sending GPIO state to Raspberry PI and store state in database.

Project is based on:
- ESP8266 and nodeMCU firmware http://www.nodemcu.com/
- raspberry Pi, minibian https://minibianpi.wordpress.com/ and flask http://flask.pocoo.org/ application
- MQTT protocal and mosquitto broker https://mosquitto.org/ for communicating between two above parts of system

nodeScripts catalog consists of scripts for nodeMCU. These scripts are responsible for handling GPIO and sending data through MQTT to raspberry. They are loaded to nodeMCU by luatool https://github.com/4refr0nt/luatool.

raspPiScripts catalog includes subscriber.py script. It handles messages from mqtt broker using paho-mqtt package. Server folder consists flask application used for api and adding sensors. config.sh is Raspberry Pi configuration draft.
