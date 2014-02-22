import MySQLdb

DATABASE = 'headacheDevDB'
DB_USER = 'dev'
DB_PASSWORD = '9Dysj'
HOST = 'localhost'

def db_connect():
  return MySQLdb.connect(HOST, DB_USER, DB_PASSWORD, DATABASE)
