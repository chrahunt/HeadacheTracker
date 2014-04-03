from wtforms import Form, StringField, PasswordField, validators
from wtforms.validators import ValidationError, StopValidation
import MySQLdb

from utils import db_connect, phash

class RegistrationForm(Form):
	username = StringField('Username', [validators.Length(min=4, max=20)])
	email = StringField('Email Address', [validators.Optional(), validators.Length(min=6, max=35), validators.Email()])
	password = PasswordField('Password', [
		validators.Required(),
		validators.EqualTo('confirm', message='Passwords must match'),
		validators.Length(min=5, max=64)
	])
	confirm = PasswordField('Repeat Password')
	first_name = StringField('First Name', [validators.Required()])
	last_name = StringField('Last Name', [validators.Required()])

	# Check that username is not already taken.
	# TODO: Check that username has proper format.
	def validate_username(form, field):
		db = db_connect()
		cur = db.cursor()

		query = "SELECT COUNT(*) FROM users WHERE l_username=LOWER('" + field.data + "')"
		cur.execute(query)

		userInfo = cur.fetchone()

		if userInfo[0] != 0:
			raise ValidationError('That username is already taken!')

class LoginForm(Form):
	username = StringField('Username', [
		validators.Length(min=4, max=20),
		validators.Required(message='Username field required.')
	])
	password = PasswordField('Password', [
		validators.Required(message='Password field required.')
	])
	
	def validate_password(form, field):
		db = db_connect()
		cur = db.cursor(MySQLdb.cursors.DictCursor)
		password = field.data

		query = "SELECT username, password_hash, salt FROM users WHERE l_username=LOWER('" + form.username.data + "')"
		cur.execute(query)

		userInfo = cur.fetchone()
		if userInfo == None:
			raise ValidationError('Invalid username.')
		else:
			possible_password_hash = phash(password + userInfo['salt'])
			if possible_password_hash != userInfo['password_hash']:
				raise ValidationError('Invalid password.')

