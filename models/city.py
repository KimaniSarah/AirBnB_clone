#!/usr/bin/python3
"""City class that inherits from BaseModel"""


from models.base_model import BaseModel


class City(BaseModel):
    """
    Public class attributes
    """
    state_id = ""
    name = ""
