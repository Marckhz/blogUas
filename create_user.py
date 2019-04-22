from flask_pymongo import PyMongo 
from flask_script import Command

from app import mongo
from app.model import User
from getpass import getpass

from app import bcrypt


class CreateUser(Command):

	def run(self):
		exit = None
		while exit is not None:
			if mongo.db.superusers.find({"username":username}):
				print("that users already exists")

				create_user = input("")
				if create_user == 'n' or 'N':
					exit = create_user

		print("Please Enter useraname and pwd")
		username = input("username: ")
		password = getpass("password: ")
		assert password == getpass("password (again): ")

		user = User(username = username, password  = bcrypt.generate_password_hash(password) )
		mongo.db.superusers.insert({"username":user.username,
							   "password":user.password})
		exit = "user added"

		print(exit)


