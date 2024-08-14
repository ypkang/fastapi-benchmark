# async_server.py

from fastapi import FastAPI, HTTPException
from motor.motor_asyncio import AsyncIOMotorClient
import asyncio
import os
import time

app = FastAPI()

client = AsyncIOMotorClient(os.getenv("DATABASE_HOST"))
db = client.test_database


@app.get("/read_and_write_item")
async def read_and_write_item(item_id: str):
    item = await db.items.find_one({"_id": item_id})
    if item is None:
        await db.items.insert_one({"_id": item_id, "data": "dummy_data"})
        return {"processed_data": "dummy_data_processed"}

    # Simulate some processing time
    time.sleep(0.1)

    # Simulate some processing before writing
    processed_data = {"processed_data": f"{item['data']}_processed"}

    # Write the processed data back to the database
    await db.items.update_one({"_id": item_id}, {"$set": processed_data}, upsert=True)

    return processed_data
