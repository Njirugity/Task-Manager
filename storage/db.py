#!/usr/bin/python3
"""Contains class Db"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, session
from sqlalchemy.orm import relationship
from models.base_model import Base
from models.user import User
from models.task import Tasks


class Db:
    def __init__(self):
        """Create connection to database"""
        self.__engine = create_engine('mysql+mysqldb://todo_user:todo_pswd@localhost/todo_db')
        Base.metadata.create_all(self.__engine)
        self.__session = None

    @property
    def _session(self):
        """Returns and SQLAlchemy session"""
        if self.__session is None:
            Session = sessionmaker(bind=self.__engine)
            self.__session = Session()
        return self.__session

    def add_user(self, username, email, password_hash):
        """
        Adds a new user to the database.

        Args:
            username (str): The username for the user.
            email (str): The email for the user.
            password_hash (str): TThe hashed password for the user.

        Returns:
            The newly created User instance.
        """
        newUser = User(username, email, password_hash)
        try:
            self._session.add(newUser)
            self._session.commit()
            return newUser
        except Exception as e:
            self._session.rollback()
            raise e
    def get_user_by_username(self, username):
        """Retrieves a user by username.

        Args:
            username (str): The username of the authenticated user to retrieve.

        Returns:
            The User instances if found ."""

        the_user = self._session.query(User).filter_by(username=username).first()
        return the_user

    def add_task(self, title, description, user_id):
        """
        Adds a new task to the database, linking it to a user.

        Args:
            title (str): The title of the task.
            description (str): The description of the task.
            user_id (str): The ID of the user (str)

        Returns:
            The newly created Tasks instance.
        """
        try:
            newTask = Tasks(title, description, user_id)

            self._session.add(newTask)
            self._session.commit()
            return newTask
        except Exception as e:
            self._session.rollback()
            raise e
    def get_task(self, user_id):
        """
        Retrieves all tasks for a given user ID.

        Args:
            user_id (str): The ID of the authenticated user.

        Returns:
            All the Tasks instances if found and belongs to the user.
        """
        tasks = self._session.query(Tasks).filter_by(user_id=user_id).all()
        return [task.to_dict() for task in tasks]

    def get_single_task(self, task_id, user_id):
        """
        Retrieves a single task by its ID, ensuring it belongs to the specified user.

        Args:
            task_id (str): The ID of the task to retrieve.
            user_id (str): The ID of the authenticated user.

        Returns:
            The Tasks instance if found and belongs to the user.
        """
        task = self._session.query(Tasks).filter_by(id=task_id, user_id=user_id).first()
        
        return task.to_dict()

    
    def update_task(self, task_id, user_id, data):
        """
        Updates an existing task for a specific user.

        Args:
            task_id (str): The ID of the task to update.
            user_id (str): The ID of the authenticated user.
            data (dict): A dictionary containing fields to update.

        Returns:
            The updated Tasks instance if successful, None if not found or unauthorized.
        """
        try:
            tasks = self._session.query(Tasks).filter_by(id=task_id, user_id=user_id).first()

            if tasks:
                tasks.title = data.get("title", tasks.title)
                tasks.description = data.get('description', tasks.description)
                tasks.completed = data.get('completed', tasks.completed)
                self._session.commit()
                return tasks
            return None
        except Exception as e:
            self._session.rollback()
            raise e

    def delete_task(self,task_id, user_id):
        """
        Deletes a task for a specific user.

        Args:
            task_id (str): The ID of the task to delete.
            user_id (str): The ID of the authenticated user.

        Returns:
            True if the task was found and deleted, False otherwise.
        """
        try:
            tasks = self._session.query(Tasks).filter_by(id=task_id, user_id=user_id).first()

            if tasks:
                self._session.delete(tasks)
                self._session.commit()
                return True

            return False
        except Exception as e:
            self._session.rollback()
            raise e
