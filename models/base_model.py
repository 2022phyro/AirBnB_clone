#!/usr/bin/python3
from _datetime import datetime
import uuid
from models import storage

class BaseModel:
    def __init__(self, *args, **kwargs):
        if len(kwargs) == 0:
            self.id = str(uuid.uuid4())
            self.created_at = datetime.now()
            self.updated_at = datetime.now()
            storage.new(self)
        else:
            for key, value in kwargs.items():
                if key == "created_at" or key == "updated_at":
                    formats = "%Y-%m-%dT%H:%M:%S.%f"
                    setattr(self, key, datetime.strptime(value, formats))
                try:
                    if key == "__class__":
                        continue
                    setattr(self, key, value)
                except KeyError:
                    continue

    def __str__(self):
        st = f"[{self.__class__.__name__}] ({self.id}) {self.__dict__}"
        return st

    def to_dict(self):
        my_obj_dict = self.__dict__
        my_obj_dict["__class__"] = self.__class__.__name__
        my_obj_dict['created_at'] = self.created_at.isoformat()
        my_obj_dict['updated_at'] = self.updated_at.isoformat()
        return my_obj_dict

    def save(self):
        self.updated_at = datetime.now()
        # storage.save()
