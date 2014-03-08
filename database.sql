DROP DATABASE IF EXISTS headacheDevDB;
CREATE DATABASE IF NOT EXISTS headacheDevDB;

GRANT ALL PRIVILEGES ON headacheDevDB.* to 'dev'@'localhost' identified by '9Dysj';

USE headacheDevDB;

DROP TABLE IF EXISTS users;
CREATE TABLE users (
	id INT NOT NULL AUTO_INCREMENT,
	username VARCHAR(50) NOT NULL,
	l_username VARCHAR(50) NOT NULL,
	password_hash CHAR(64) NOT NULL,
	salt CHAR(12) NOT NULL,
	first_name VARCHAR(50),
	last_name VARCHAR(50),
	PRIMARY KEY(id)
);

