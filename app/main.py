from fastapi import FastAPI
from app.api import example
from app.db import db

app = FastAPI(title='Monday Hackathon')

@app.on_event("startup")
async def startup():
    await db.connect()

@app.on_event("shutdown")
async def shutdown():
    await db.disconnect()

app.include_router(example.router)
