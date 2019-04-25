from flask import Flask
from flask_bootstrap import Bootstrap
from flask_wtf.csrf import CSRFProtect

from flask_pymongo import PyMongo 
from flask_login import LoginManager
from flask_bcrypt import Bcrypt 
import urllib.parse


app = Flask(__name__)

boostrap = Bootstrap()
csrf = CSRFProtect()
login_manager = LoginManager()
bcrypt = Bcrypt()


username = urllib.parse.quote_plus('marco')
password = urllib.parse.quote_plus('metallica1')

app.config['MONGO_URI'] = 'mongodb+srv://%s:%s@uas-6xetc.mongodb.net/test?retryWrites=true' %(username, password)

mongo = PyMongo(app)

from app.views import page

def create_app(config):

	app.config.from_object(config)


	boostrap.init_app(app)
	csrf.init_app(app)
	login_manager.init_app(app)
	bcrypt.init_app(app)

	app.register_blueprint(page)

	return app