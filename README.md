
REST API for giving quote of the day message to users.\
\
Front End: HTML\
Back End: Python\
Framework: Flask\
Database: MySQL\
\
Execute the following MySQL code in your database:\
\
CREATE DATABASE IF NOT EXISTS `myDatabase`;\
USE `myDatabase`;\
CREATE TABLE IF NOT EXISTS `quotes` (\
	`id` INT(11) NOT NULL PRIMARY KEY AUTO_INCREMENT,\
  `quote` VARCHAR(255)\
);
