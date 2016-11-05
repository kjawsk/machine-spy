from flask import Flask, jsonify

app = Flask(__name__)


@app.route('/')
def index():
    return 'Flask is not running!'


@app.route('/data')
def names():
    data = {"names": ["John", "Karol", "Anna", "Jacob", "Julie", "Jennifer"]}
    return jsonify(data)

if __name__ == '__main__':
    app.run()
