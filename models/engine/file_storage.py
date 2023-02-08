#!/usr/bin/python3
import json


class FileStorage:
    __file_path = "test.json"
    __objects = {}

    def all(self):
        return FileStorage.__objects


    def new(self, obj):
        key = f"{obj.__class__.__name__}.{obj.id}"
        self.all().update({key: obj})

    def save(self):
        with open(FileStorage.__file_path, 'w') as save:
            to__dict = {}
            to__dict.update(FileStorage.__objects)
            for key, value in to__dict.items():
                to__dict[key] = value.to_dict()
            json.dump(to__dict, save)
    def reload(self):
        try:
            from models.base_model import BaseModel
            text = {}
            with open(self.__file_path, 'r') as reload:
                text = json.load(reload)
                for key, value in text.items():
                    self.all()[key] = BaseModel(**value)
        except IOError:
            pass


