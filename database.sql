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
	email VARCHAR(64),
	PRIMARY KEY(id)
);

DROP TABLE IF EXISTS headache_entries;
CREATE TABLE headache_entries (
	id INT NOT NULL AUTO_INCREMENT,
	entry_start DATETIME NOT NULL,
	entry_end DATETIME NULL,
	severity INT NOT NULL,
	user_id INT NOT NULL,
	CONSTRAINT headache_entry_user_id_fk
	FOREIGN KEY (user_id)
	REFERENCES users (id),
	PRIMARY KEY(id)
);
