from pymongo import MongoClient
from .settings import settings


# MongoDB setup
client = MongoClient(settings.database_url)
db = client['dataapp']
