#!/usr/bin/python3
"""This initializes the storage variable for the console"""
from models.engine.file_storage import FileStorage
storage = FileStorage()
storage.reload()
