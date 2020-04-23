--create_db.sql
DROP TABLE IF EXISTS user;

CREATE TABLE user (email text,password text,groups text);