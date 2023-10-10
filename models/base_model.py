#!/usr/bin/python3
"""BaseModel class"""


import models
from uuid import uuid4
from datetime import datetime


class BaseModel:
    """defines all common attributes/methods for other classes"""
    def __init__(self, *args, **kwargs):
        """initializes public instance attributes"""
        if not kwargs:
            self.id = str(uuid4())
            self.created_at = datetime.now()
        else:
            self.id = kwargs.get('id', str(uuid4()))
            self.created_at = kwargs.get('created_at', datetime.now())

        self.update_at = datetime.now()

        for key, value in kwargs.items():
            if key != "__class__":
                if key in ('created_at', 'update_at'):
                    setattr(self, key, datetime.fromisoformat(value))
                else:
                    setattr(self, key, value)

    def __str__(self):
        return f"[{self.__class__.__name__}] ({self.id}) {self.__dict__}"

    def save(self):
        """updates the public instance attribute update_at
        with the current datetime"""
        self.update_at = datetime.now()

    def to_dict(self):
        """returns a dictionary containing all key/values
        of __dict__ of the instance"""
        my_dict = self.__dict__.copy()
        my_dict['__class__'] = self.__class__.__name__
        my_dict['created_at'] = self.created_at.isoformat()
        my_dict['update_at'] = self.update_at.isoformat()
        return my_dict
