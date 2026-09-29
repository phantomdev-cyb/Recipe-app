from sqlalchemy import Column, Integer,String, Text, Table,DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .database import sqlClass

class Favourite(sqlClass):
  __tablename__="Favourites"
  id=Column(Integer,primary_key=True, index=True)
  meal_id=Column(String,index=True, nullable=True)
  created_at=Column(DateTime(timezone=True),server_default=func.now())
  title=Column(String, nullable=False, index=True)
  recipe=Column(Text,index=True, nullable=False)
  thumbnail=Column(String, nullable=True)
  yt_link=Column(String, nullable=True)
  ingredients=Column(Text,index=True, nullable=True)