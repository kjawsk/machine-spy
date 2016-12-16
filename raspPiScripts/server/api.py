from flask import request, json, render_template, flash, url_for
from server import app
import datetime

@app.route('/')
def index():
    return 'Hello World!'

@app.route('/messages', methods = ['POST'])
def api_message():
    if request.headers['Content-Type'] == 'application/json':
        print (request.json)
        return "JSON Message: " + json.dumps(request.json)
    else:
        return "415 Unsupported Media Type ;)"
