from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from models.base_model import Base, BaseModel

class Tasks(BaseModel, Base):
    __tablename__ = "tasks"
    title = Column(String, nullable=False)
    description = Column(String, nullable=True)
    completed = Column(Boolean, default=False)
    user_id = Column(String(60), ForeignKey("users.id"), nullable=False)

    def __init__(self,title, description,completed,user_id, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title = title
        self.description = description
        self.completed = completed
        self.user_id = user_id

