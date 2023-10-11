#!/usr/bin/python3
"""
a class for  serialization-deserialization of
instances to and from a JSON file
"""


import json
import locale
from models.amenity import Amenity
from models.user import User
from models.base_model import BaseModel
from models.state import State
from models.place import Place
from models.review import Review
from models.city import City


class FileStorage:
    """
    serializes instances to a JSON file, deserializes JSON file to instances
    __file_path: string - path to the JSON file
    __objects: dictionary - empty but store all objects by <class name>.id
    """
    __file_path = "file.json"
    __objects = {}

    def all(self):
        """returns the dictionary __objects"""
        return FileStorage.__objects

    def new(self, obj):
        """sets in __objects the obj with key <obj class name>.id"""
        obClname = obj.__class__.__name__
        FileStorage.__objects["{}.{}".format(obClname, obj.id)] = obj

    def save(self):
        """serializes __objects to the JSON file (path: __file_path)"""
        with open(FileStorage.__file_path, "w", encoding="utf-8") as f:
            nd = {ky: vl.to_dict() for ky, vl in FileStorage.__objects.items()}
            json.dump(nd, f)

    def reload(self):
        """
        deserializes the JSON file to __objects if the JSON file (__file_path) exists
        """

        classes = {"BaseModel": BaseModel,
                   "Place": Place,
                   "City": City,
                   "User": User,
                   "Review": Review,
                   "Amenity": Amenity,
                   "State": State
                   }
        try:
            with open(FileStorage.__file_path, "r", encoding="utf-8") as f:
                nd = json.load(f)
                for ky, vl in nd.items():
                    obClname, obj_id = ky.split(".")
                    FileStorage.__objects[ky] = globals()[obClname](**vl)
        except FileNotFoundError:
            return
