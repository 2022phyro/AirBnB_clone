#!/usr/bin/python3
"""This file contains the basemodel class"""
from _datetime import datetime
import uuid


class BaseModel:
    """This is the basemodel class"""
    def __init__(self, *args, **kwargs):
        """This initializes the basemodel class"""
        if not kwargs:
            from models import storage
            self.id = str(uuid.uuid4())
            self.created_at = datetime.now()
            self.updated_at = datetime.now()
            storage.new(self)
        else:
            formats = "%Y-%m-%dT%H:%M:%S.%f"
            kwargs['created_at'] = datetime.strptime(
                kwargs['created_at'], formats)
            kwargs['updated_at'] = datetime.strptime(
                kwargs['updated_at'], formats)
            if '__class__' in kwargs.keys():
                del kwargs['__class__']
            self.__dict__.update(kwargs)

    def __str__(self):
        """This overrides str to print a string representation of the class"""
        st = f"[{self.__class__.__name__}] ({self.id}) {self.__dict__}"
        return st

    def to_dict(self):
        """Returns a dict representation of the class"""
        my_obj_dict = {}
        my_obj_dict.update(self.__dict__)
        my_obj_dict.update({"__class__": self.__class__.__name__})
        my_obj_dict['created_at'] = self.created_at.isoformat()
        my_obj_dict['updated_at'] = self.updated_at.isoformat()
        return my_obj_dict

    def save(self):
        """Saves an instance to the storage file"""
        from models import storage
        self.updated_at = datetime.now()
        storage.save()
