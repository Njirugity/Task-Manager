CREATE DATABASE IF NOT EXISTS todo_db;

CREATE USER IF NOT EXISTS 'todo_user' @'localhost' IDENTIFIED BY 'todo_pswd';

GRANT ALL PRIVILEGES ON todo_db.* TO 'todo_user' @'localhost';

FLUSH PRIVILEGES;