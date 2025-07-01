from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from models.base_model import Base, BaseModel

class User(BaseModel,Base):

    __tablename__ = "users"

    username = Column(String(128), unique=True, nullable=False)
    email = Column(String(128), unique=True, nullable=False)
    password_hash = Column(String(128), nullable=False)

    taskRlt = relationship('Tasks', back_populates="userRlt")

    def __init__(self, username, email, password_hash,*args, **kwargs):
        
        super().__init__(*args, **kwargs)
        self.username = username
        self.email = email
        self.password_hash = password_hash