from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker,declarative_base

DATABASE_URL="sqlite:///.recipes.db"
engine=create_engine(DATABASE_URL,connect_args={"check_same_thread": False})
Session=sessionmaker(autocommit=False, autoflush=False, bind=engine)
sqlClass=declarative_base()

def get_db():
  db=Session()
  try:
    yield db
  finally:
    db.close()