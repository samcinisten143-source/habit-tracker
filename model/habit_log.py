from sqlalchemy import Column, Integer, Boolean, Date, ForeignKey
from sqlalchemy.orm import relationship
from database.db_session import Base

class HabitLog(Base):
    __tablename__ = "habit_logs"

    id = Column(Integer, primary_key=True, index=True)

    # Link to habit
    habit_id = Column(Integer, ForeignKey("habits.id", ondelete="CASCADE"), nullable=False)

    # Link to user
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

    date = Column(Date, nullable=False)
    completed = Column(Boolean, default=False)

    # Relationships
    habit = relationship("Habit", back_populates="logs")
    user = relationship("User", back_populates="habit_logs")
