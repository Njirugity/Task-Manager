#!/usr/bin/python3
"""Contains class BaseModel"""

from datetime import datetime
from sqlalchemy import Column, String, Integer, DateTime
from sqlalchemy.orm import declarative_base
import uuid

time = "%Y-%m-%dT%H:%M:%S.%f"

Base = declarative_base()


class BaseModel:
    """The BaseModel class from which future classes
    will be derived"""

    id = Column(String(60), primary_key=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __init__(self, *args, **kwargs):
        """Initialization of the base model"""
        self.id = str(uuid.uuid4())
        self.created_at = datetime.utcnow()
        self.updated_at = self.created_at

    def to_dict(self):
        """
        Converts the model instance to a dictionary
        """
        new_dict = self.__dict__.copy()
        if "created_at" in new_dict:
            new_dict["created_at"] = new_dict["created_at"].strftime(time)
        if "updated_at" in new_dict:
            new_dict["updated_at"] = new_dict["updated_at"].strftime(time)
        if "_sa_instance_state" in new_dict:
            del new_dict["_sa_instance_state"]
        if "password_hash" in new_dict:
            del new_dict["password_hash"]

        return new_dict
