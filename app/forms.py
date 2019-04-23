from wtforms import Form,validators
from wtforms import StringField, SelectField, FileField, DateField
from wtforms.widgets import TextArea

#import date


class LoginForm(Form):

	username = StringField('username', [validators.Length(min=6, max = 50)] )
	password = StringField('password', [validators.Length(min=6, max = 50)] )



class NewPost(Form):

	title = StringField('Titulo', [validators.Length(min=1, max = 50)] )
	body = StringField('Contentido', [validators.Length(min=1, max= 10000000)], widget= TextArea())
