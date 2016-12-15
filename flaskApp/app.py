from flask import request
from flask import json
from flask import render_template
from flask import flash
import datetime

from flask import Flask, url_for
app = Flask(__name__)
app.secret_key = 'some_secret'


# REST Server Welcome Message
@app.route('/')
@app.route('/<name>')
def api_root(name=None):
    return render_template('hello.html', name=name)

# POST receive message, sends back json data in response
@app.route('/messages', methods = ['POST'])
def api_message():
    if request.headers['Content-Type'] == 'application/json':
        # For demo purposes print out received json
        print (request.json)
        f = open("file", "a")
        f.write(str(datetime.datetime.now()) + json.dumps(request.json) + "\n")
        f.close()
        return "JSON Message: " + json.dumps(request.json)
    else:
        return "415 Unsupported Media Type ;)"

if __name__ == '__main__':
    app.run()
