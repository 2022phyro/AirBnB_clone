#!/usr/bin/python3
from models import storage
from models.base_model import BaseModel


my_model = BaseModel()
my_model.name = "My_First_Model"
my_model.my_number = 89
my_model.save()
print(my_model.__dict__)