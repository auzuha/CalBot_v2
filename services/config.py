from services.database import engine
from models.schemas import Base
from dotenv import load_dotenv


Base.metadata.create_all(engine)





load_dotenv()