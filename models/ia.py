from bson import ObjectId
from pydantic import BaseModel
from pydantic_mongo import  PydanticObjectId
from pymongo import MongoClient
from datetime import datetime
from typing import Optional, List
import os


class Completion(BaseModel):
  source: str = ""
  option: str = ""
  prompt: str = ""