# app/database.py

from motor.motor_asyncio import AsyncIOMotorClient
from os import environ as env

DB_URL = env.get("DB_URL")
Dbclient = AsyncIOMotorClient(DB_URL)
Cluster = Dbclient["Cluster0"]
Data = Cluster["users"]