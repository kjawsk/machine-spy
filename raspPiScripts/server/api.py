from flask import request
from server import app
from server.models import db, Entry

def add_to_db(item):
    db.session.add(item)
    db.session.commit()

@app.route('/')
def index():
    return 'Main page!'

@app.cli.command('initdb')
def initdb_command():
    """Creates the database tables"""
    db.create_all()
    print('Initialized the database.')

@app.route('/entries', methods=['POST'])
def add_entry():
    if request.headers['Content-Type'] == 'application/json':
        content = request.get_json(silent=True)
        new_entry = Entry(content['sensor_name'], content['value'])
        add_to_db(new_entry)
        return 'Entry added: ' + str(content)
    return '415 Unsupported Media Type'
