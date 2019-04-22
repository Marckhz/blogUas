from wtforms import Form,validators
from wtforms import StringField, SelectField, FileField
from wtforms.widgets import TextArea




class LoginForm(Form):

	username = StringField('username', [validators.Length(min=6, max = 50) ])
	password = StringField('password', [validators.Length(min=6, max = 50)])

