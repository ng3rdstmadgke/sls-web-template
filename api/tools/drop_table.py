from api.db.db import engine
from api.db.base import Base

Base.metadata.drop_all(bind=engine)