from sqlalchemy import Column, Integer, String
from database.db_session import Base

class Sample(Base):
    __tablename__ = "sample"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
