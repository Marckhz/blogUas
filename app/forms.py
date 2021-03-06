from wtforms import Form,validators
from wtforms import StringField, SelectField, FileField, DateField
from wtforms.widgets import TextArea

#import date


class LoginForm(Form):

	username = StringField('username', [validators.required(),  validators.Length(min=6, max = 50)] )
	password = StringField('password', [validators.required(), validators.Length(min=6, max = 50)] )



class NewPost(Form):

	title = StringField('Titulo', [validators.required(),  validators.Length(min=1, max = 50)] )
	body = StringField('Contentido', [validators.required(), validators.Length(min=1, max= 10000000)], widget= TextArea())
	category =  SelectField('Categoria', choices=[('Academica', 'Academica'), ('Cultural', 'Cultural'), ('Deportiva', 'Deportiva') ])


class TeamForm(Form):

	name = StringField('Nombre', [validators.required(), validators.Length(min=4, max=20)] )
	departament = SelectField('Departamento', choices = [
												('Direccion', 'Direccion'), 
												('Secreteria Academica','Secreataria Academica'), 
												('Secretaria Administrativa', 'Secreataria Administrativa'),
												('Control Escolar', 'Control Escolar'), 
												('Servicio Social', 'Servicio Social'),
												('Tutorias', 'Tutorias'),
												('Orientacion', 'Orientacion Educativa'),
												('Biblioteca', 'Biblioteca'),
												('Difusion Cultural', 'Difusion Cultural'),
												('Centro de Computo', 'Centro de Computo'),
												('Sustentabilidad', 'Sustentabilidad'),
												('Mantenimiento', 'Mantenimiento'),
												('Extension Villajuarez', 'Extension Villa Juarez'),
												('Extension Sataya','Extension Sataya') 
												] 
							)
	charge = StringField('Cargo', [validators.required(), validators.Length(min=1, max=50)])
	phone = StringField('Numero Telefonico', [validators.required(), validators.Length(min=10, max=10)])
	email = StringField('Correo Electronico', [validators.required(), validators.Length(min=6, max=50)])