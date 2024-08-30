# async_server.py

from fastapi import FastAPI, HTTPException
from motor.motor_asyncio import AsyncIOMotorClient
import asyncio
import os
import time
import random

app = FastAPI()

client = AsyncIOMotorClient(os.getenv("DATABASE_HOST"))
db = client.test_database


def cpu_bound_task():
    # Simulate a CPU-bound task
    result = 0
    for i in range(10**6):
        result += i * i
    return result


@app.get("/read_and_write_item")
async def read_and_write_item() -> dict:
    for item_id in range(20):
        item = await db.items.find_one({"_id": str(item_id)})
        if item is None:
            await db.items.insert_one({"_id": str(item_id), "data": "dummy_data"})

    # Simulate some processing time
    # time.sleep(0.05)
    cpu_bound_task()

    # Write half the processed data back to the database
    for item_id in range(20):
        if random.choice([True, False]):
            # Simulate some processing before writing
            processed_data = {"processed_data": f"{item_id} processed"}

            await db.items.update_one(
                {"_id": str(item_id)}, {"$set": processed_data}, upsert=True
            )

    return processed_data
