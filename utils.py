import MySQLdb
import random
import hashlib

DATABASE = 'headacheDevDB'
DB_USER = 'dev'
DB_PASSWORD = '9Dysj'
HOST = 'localhost'

BASE64LETTERS = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789/+"

def db_connect():
	return MySQLdb.connect(HOST, DB_USER, DB_PASSWORD, DATABASE)

# Generate a salt of length `length`, default 12 when no arguments are passed.
def get_salt(length = 12):
	salt_letters = []
	for i in range(length):
		salt_letters.append(random.choice(BASE64LETTERS))
	
	salt = ''.join(salt_letters)
	return salt

# Password-hashing function, returns hex digest for insertion into db
def phash(str):
	return hashlib.sha256(str).hexdigest()
