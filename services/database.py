from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from models.schemas import Base

engine = create_engine('sqlite:///database.db', echo=False)

Session = sessionmaker(bind=engine)

session = scoped_session(Session)
