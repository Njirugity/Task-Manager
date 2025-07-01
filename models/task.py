from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from models.base_model import Base, BaseModel

class Tasks(BaseModel, Base):
    __tablename__ = "tasks"

    title = Column(String(256), nullable=False)
    description = Column(String(500), nullable=True)
    completed = Column(Boolean, default=False)
    user_id = Column(String(60), ForeignKey("users.id"), nullable=False)

    userRlt = relationship('User', back_populates="taskRlt")

    def __init__(self,title, description,user_id, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title = title
        self.description = description
        
        self.user_id = user_id

