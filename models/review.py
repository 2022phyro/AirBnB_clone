#!/usr/bin/python3
"""This file contains the review class"""
from models.base_model import BaseModel


class Review(BaseModel):
    """A class for reviews"""
    place_id = ""
    user_id = ""
    text = ""
