from api.db.db import engine
from api.db.base import Base

Base.metadata.create_all(bind=engine)