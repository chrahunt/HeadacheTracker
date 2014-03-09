from wtforms import Form, StringField, PasswordField, validators, ValidationError
from utils import db_connect

class RegistrationForm(Form):
	username = StringField('Username', [validators.Length(min=4, max=20)])
	email = StringField('Email Address', [validators.Optional(), validators.Length(min=6, max=35), validators.Email()])
	password = PasswordField('Password', [
		validators.Required(),
		validators.EqualTo('confirm', message='Passwords must match')
	])
	confirm = PasswordField('Repeat Password')
	
	# Check that username is not already taken.
	# TODO: Check that username has proper format.
	def validate_username(form, field):
		db = db_connect()
		cur = db.cursor()

		query = "SELECT COUNT(*) FROM users WHERE l_username=LOWER('" + field.data + "')"
		cur.execute(query)

		userInfo = cur.fetchone()
		print userInfo

		if userInfo[0] != 0:
			raise ValidationError('That username is already taken!')

