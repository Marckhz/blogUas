from werkzeug.security import check_password_hash
from flask_login import UserMixin


class User(UserMixin):

	def __init__(self, username):

		self.username = username

	def is_authenticated():
		return True

	def is_active(self):
		return True

	def get_id(self):

		return self.username

	@staticmethod
	def validate_login(password_hash, password):
		return check_password_hash(password_hash, password)