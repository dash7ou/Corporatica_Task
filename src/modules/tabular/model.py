from pymongo import MongoClient
import pandas as pd
import json
from bson import ObjectId

class DatasetModel:
    def __init__(self, db):
        self.collection = db['tabular']

    def save_dataset(self, data, name):
        records = json.loads(data.to_json(orient='records'))
        return self.collection.insert_one({"name": name, "data": records}).inserted_id

    def get_dataset(self, dataset_id):
        doc = self.collection.find_one({"_id": ObjectId(dataset_id)})
        if doc:
            return pd.DataFrame(doc['data'])
        return None

    def update_dataset(self, dataset_id, updated_data):
        return self.collection.update_one({"_id": ObjectId(dataset_id)}, {"$set": {"data": updated_data}})

    def delete_dataset(self, dataset_id):
        return self.collection.delete_one({"_id": ObjectId(dataset_id)})
    
    def list_datasets(self):
        datasets = self.collection.find({}, {"name": 1})
        return [{"id": str(dataset['_id']), "name": dataset['name']} for dataset in datasets]
