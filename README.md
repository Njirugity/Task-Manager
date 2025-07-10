# Task Manager Web Application

This application is for individuals how have multiple tasks to perfom but do have a place to list the down.
It is a web based appliccation that allows the user to list down their tasks

## Features

- Register to be a user and get an account
- Login to your account
- Add all you new tasks
- Veiw all your tasks on the home page
- Mark completed tasks
- Delete any task

## Installation

The application is a based on Flask 3.1.1

- Clone the repository using `git clone`
- Navigate to the project directory using `cd Task-manager`
- Create a virual environment using `python3 -m venv .env`
- Activate the virtual environment using `source .env/bin/activate`
- Run `pip install -r requirements.txt` to install the dependancies
- Set up a new blank databse using `mysql -u root -p < setup_db.sql`
- Run `python3 app.py` to start the server
- Navigae to `http://127.0.0.1:5000` to access the application
- To view the database run `mysql -u todo_user -p todo_db` password is `todo_pswd`
