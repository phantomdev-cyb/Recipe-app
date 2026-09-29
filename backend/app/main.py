from fastapi import FastAPI
from .route import favourite
from . import model
from .database import engine, sqlClass

model.sqlClass.metadata.create_all(bind=engine)
app=FastAPI()
app.include_router(favourite.router)
