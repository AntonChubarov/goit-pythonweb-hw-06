from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import atexit

engine = create_engine('postgresql://postgres:hw6pwd@localhost:5432/postgres')
Session = sessionmaker(bind=engine)
session = Session()

def close_session():
    session.close()

atexit.register(close_session)
