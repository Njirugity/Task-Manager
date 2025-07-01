from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, session
from sqlalchemy.orm import relationship
from models.base_model import Base
from models.user import User
from models.task import Tasks


class Db:
    def __init__(self):
        self.__engine = create_engine('mysql+mysqldb://todo_user:todo_pswd@localhost/todo_db')
        Base.metadata.create_all(self.__engine)
        self.__session = None
    
    @property
    def _session(self):
        if self.__session is None:
            Session = sessionmaker(bind=self.__engine)
            self.__session = Session()
        return self.__session
    
    def add_user(self, username, email, password_hash):
        newUser = User(username, email,password_hash)

        self._session.add(newUser)
        self._session.commit()
        return newUser
    
    def get_user_by_username(self, username):
        the_user = self._session.query(User).filter_by(username=username).first()
        return the_user

    def add_task(self, title, description, user_id):
        newTask = Tasks(title, description, user_id)
        self._session.add(newTask)
        self._session.commit()
        return newTask