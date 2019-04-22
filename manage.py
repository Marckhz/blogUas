from app import create_app
from flask_script import Manager, Server
from config import config

from create_user import CreateUser


config_class = config['development']

app = create_app(config_class)

createsuperuser = CreateUser()


if __name__ == '__main__':
	manager = Manager(app)
	manager.add_command("createsuperuser", createsuperuser)
	manager.add_command("runserver", Server('0.0.0.0') )
	manager.run()
