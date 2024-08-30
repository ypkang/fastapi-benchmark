# sync_server.py

import time
import os
import random

from fastapi import FastAPI
from pymongo import MongoClient

app = FastAPI()

client = MongoClient(os.getenv("DATABASE_HOST"))
db = client.test_database


@app.get("/read_and_write_item")
def read_and_write_item() -> dict:
    for item_id in range(20):
        item = db.items.find_one({"_id": str(item_id)})
        if item is None:
            db.items.insert_one({"_id": str(item_id), "data": "dummy_data"})

    # Simulate a CPU task, e.g. AI
    time.sleep(0.05)

    # Write half the processed data back to the database
    for item_id in range(20):
        if random.choice([True, False]):
            # Simulate some processing before writing
            processed_data = {"processed_data": f"{item_id} processed"}

            db.items.update_one(
                {"_id": str(item_id)}, {"$set": processed_data}, upsert=True
            )

    return processed_data
