# sync_server.py

from fastapi import FastAPI, HTTPException
from pymongo import MongoClient
import time
import os

app = FastAPI()

client = MongoClient(os.getenv("DATABASE_HOST"))
db = client.test_database


@app.get("/read_and_write_item")
def read_and_write_item(item_id: str):
    item = db.items.find_one({"_id": item_id})
    if item is None:
        db.items.insert_one({"_id": item_id, "data": "dummy_data"})
        return {"processed_data": "dummy_data_processed"}

    # Simulate some processing time
    time.sleep(0.1)

    # Simulate some processing before writing
    processed_data = {"processed_data": f"{item['data']}_processed"}

    # Write the processed data back to the database
    db.items.update_one({"_id": item_id}, {"$set": processed_data}, upsert=True)

    return processed_data
