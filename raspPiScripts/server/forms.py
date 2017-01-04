from wtforms import Form, StringField, PasswordField, validators

class AddSensorForm(Form):
    name = StringField(
        'Name',
        [validators.Length(
            min=15,
            max=15,
            message='Name must be 15 character long')])

class LoginForm(Form):
    username = StringField('Username', [validators.DataRequired()])
    password = PasswordField('Password', [validators.DataRequired()])
