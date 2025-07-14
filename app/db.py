from beanie import init_beanie
from app.models import Movie, MovieUpdate, User
import motor.motor_asyncio
import os

MONGO_HOST=os.getenv("MONGO_HOST")
MONGO_USER=os.getenv("MONGO_USER")
MONGO_PASS=os.getenv("MONGO_PASS")
MONGO_PORT=os.getenv("MONGO_PORT")
MONGO_DB=os.getenv("MONGO_DB")

async def init_db():
    MONGO_URI = f"mongodb://{MONGO_USER}:{MONGO_PASS}@{MONGO_HOST}:{MONGO_PORT}/{MONGO_DB}"
    client = motor.motor_asyncio.AsyncIOMotorClient(
        MONGO_URI
    )
    #client = motor.motor_asyncio.AsyncIOMotorClient(
    #    "mongodb+srv://<username>:<password>@cluster0.zlhkso0.mongodb.net/?retryWrites=true&w=majority"
    #)

    await init_beanie(database=client[MONGO_DB], document_models=[Movie, User])
