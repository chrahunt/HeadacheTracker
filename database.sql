DROP DATABASE IF EXISTS headacheDevDB;
CREATE DATABASE IF NOT EXISTS headacheDevDB;

GRANT ALL PRIVILEGES ON headacheDevDB.* to 'dev'@'localhost' identified by '9Dysj';

USE headacheDevDB;

DROP TABLE IF EXISTS users;
CREATE TABLE users (
	id INT NOT NULL AUTO_INCREMENT,
	username VARCHAR(50) NOT NULL,
	password VARCHAR(50) NOT NULL,
	first_name VARCHAR(50),
	last_name VARCHAR(50),
	PRIMARY KEY(id)
);

-- Test user.
INSERT INTO users (username, password, first_name, last_name) VALUES
	('a', 'a', 'John', 'Smith'),
	('b', 'b', 'Jane', 'Smith');
