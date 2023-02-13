#!/usr/bin/python3
"""This file contains the review class"""
from models.base_model import BaseModel


class Review(BaseModel):
    """This is the Review class"""
    place_id = ""
    user_id = ""
    text = ""
