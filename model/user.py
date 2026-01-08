from sqlalchemy import Column, Integer, String,DateTime
from sqlalchemy.orm import relationship
from database.db_session import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    last_login = Column(DateTime(timezone=True), nullable=True)


    # One user → many habits
    habits = relationship(
        "Habit",
        back_populates="user",
        cascade="all, delete-orphan"
    )

    # One user → many habit logs
    habit_logs = relationship(
        "HabitLog",
        back_populates="user",
        cascade="all, delete-orphan"
    )
