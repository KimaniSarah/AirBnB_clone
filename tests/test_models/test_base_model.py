#!/usr/bin/python3
"""tests the functions"""


import unittest
from uuid import uuid4
from datetime import datetime
from models.base_model import BaseModel

class test_BaseModel(unittest.TestCase):
    def test_init_no_args(self):
        obj = BaseModel()
        self.assertIsInstance(obj.id, str)
        """check if the id is a string"""
        self.assertIsInstance(obj.created_at, datetime)
        """check if the created_at is a datetime"""
        self.assertIsInstance(obj.updated_at, datetime)
        """check if the updated_at is a datetime"""

    def test_init_with_kwargs(self):
        example_created_at = '2017-09-28T21:03:54.052302'
        kwargs = {
                'created_at' : example_created_at,
                'name' : 'spongebob'
                }
        """"the above is an example scenerio in order to test"""
        obj = BaseModel(**kwargs)
        """used double asterisk to unpack a dictionary"""

        self.assertIsInstance(obj.updated_at, datetime)
        self.assertEqual(obj.created_at, datetime.fromisoformat(example_created_at))
        self.assertEqual(obj.name, 'spongebob')

    def test_save(self):
        """i created an instance then stored its updated_at then called the
        save method ,which is supposed to update the updated_at thus the original
        updated_at and after calling save should be different"""
        obj = BaseModel()
        initial_updated_at = obj.updated_at
        obj.save()
        self.assertNotEqual(initial_updated_at, obj.updated_at)

    def test_to_dict(self):
        obj = BaseModel()
        my_dict = obj.to_dict()
        self.assertIsInstance(my_dict, dict)
        self.assertIsInstance(my_dict['created_at'], str)
        self.assertIsInstance(my_dict['updated_at'], str)
        self.assertEqual(my_dict['__class__'], 'BaseModel')
