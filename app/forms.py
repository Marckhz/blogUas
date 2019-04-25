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


class TeamForm(Form):

	name = StringField('Nombre', [validators.Length(min=4, max=20)] )
	position = SelectField('Puesto', choices = [
												('Direccion, Direccion'), 
												('SecreteriaAcademica','Secreataria Academica'), 
												('SecretariaAdministrativa', 'Secreataria Administrativa')
												('ControlEscolar', 'Control Escolar'), 
												('ServicioSocial', 'Servicio Social'),
												('Tutorias, Tutorias'),
												('Orientacion', 'Orientacion Educativa'),
												('Biblioteca', 'Biblioteca'),
												('DifusionCultural', 'Difusion Cultural'),
												('CentrodeComputo', 'Centro de Computo'),
												('Sustentabilidad', 'Sustentabilidad'),
												('Mantenimiento', 'Mantenimiento'),
												('ExtensionVillajuarez', 'Extension Villa Juarez'),
												('ExtensionSataya','Extension Sataya') 
												] 
							)
	phone = StringField('Numero Telefonico', [validators.Length(min=10, max=10)])
	email = StringField('Correo Electronico', [validators.Length(min=6, max=50)])