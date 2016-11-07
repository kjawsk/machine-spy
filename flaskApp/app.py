from flask import request
from flask import json

from flask import Flask, url_for
app = Flask(__name__)

# REST Server Welcome Message
@app.route('/')
def api_root():
    return 'Welcome to the DEMO REST Server'

# POST receive message, sends back json data in response
@app.route('/messages', methods = ['POST'])
def api_message():
    if request.headers['Content-Type'] == 'application/json':
        # For demo purposes print out received json
        print request.json
        return "JSON Message: " + json.dumps(request.json)
    else:
        return "415 Unsupported Media Type ;)"

if __name__ == '__main__':
    app.run()
