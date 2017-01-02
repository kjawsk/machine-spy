from wtforms import Form, StringField, validators

class AddSensorForm(Form):
    name = StringField('Name', [validators.Length(min=15, max=15)])
