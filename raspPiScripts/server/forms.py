from wtforms import Form, StringField, PasswordField, validators
from wtforms.validators import DataRequired, Length
from .util.validators import Unique
from .models import Sensor

class AddSensorForm(Form):
    name = StringField(
        'Name',
        validators=[
            Length(
                min=15,
                max=15,
                message='Name must be 15 character long'),
            Unique(
                Sensor,
                Sensor.name,
                message='Sensor already exist, name is not unique')
        ])

class LoginForm(Form):
    username = StringField('Username', [validators.DataRequired()])
    password = PasswordField('Password', [validators.DataRequired()])
