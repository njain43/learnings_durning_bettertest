from unittest import TestCase
from pathlib import Path

from pymongo import MongoClient

from src.converter_indexer import samples
from src.converter_indexer.converter import Converter
import json


class TestMongoDBconnection(TestCase):

    def setUp(self) -> None:
        # Connect to MongoDB
        self.client = MongoClient("mongodb://localhost:27017/")
        self.db = self.client["test_database"]  # creating a databased named client
        self.db_obj = self.db["users"]

    def test_insert_data(self):
        user_data = {"name": "Nitesh", "age": 35, "city": "Pune"}
        multi_user_data = [
            {"name": "Nitesh", "age": 35, "city": "Pune", "area": "Kharadi"},
            {"name": "Sachin", "age": 40, "city": "Satara"},
            {"name": "Pratik", "age": 30, "city": "Indore"},
        ]

        self.db_obj.insert_one(user_data)
        self.db_obj.insert_many(multi_user_data)

    def test_update_data(self):
        # self.db_obj.update_one({"name": "Nitesh"}, {"$set": {"position": "Senior Manager"}})
        self.db_obj.update_one({"position": "Senior Manager"}, {"$set": {"name": "Rahul"}})



    def test_retreive_data(self):
        res = self.db_obj.find_one({"name": "Nitesh"})
        print(f'using find_one {res}')

        # using find_one
        for i, usr in enumerate(self.db_obj.find({"name": "Nitesh"})):
            print(i, usr)
