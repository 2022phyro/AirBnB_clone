#!/usr/bin/python3
import json


class FileStorage:
    __file_path = "file.json"
    __objects = {}

    def all(self):
        return self.__objects

    def new(self, obj):
        key = f"{obj.__class__.__name__}.{obj.id}"
        self.__objects[key] = obj

    def save(self):
        self.reload()
        the_json_dict = {}
        for key, value in self.__objects.items():
            the_json_dict[key] = value.to_dict()
        with open(self.__file_path, "w") as store:
            json.dump(the_json_dict, store)

    def reload(self):
        # try:
        #     with open(self.__file_path, 'r') as reload:
        #         the_json_store = json.load(reload)
        #         for key, value in the_json_store.items():
        #             if key in self.__objects.keys():
        #                 self.__objects[key].__init__(value)
        # except IOError:
        #     pass
        pass

