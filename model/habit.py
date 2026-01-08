from sqlalchemy import Column, Integer, String, DateTime, func, ForeignKey
from sqlalchemy.orm import relationship
from database.db_session import Base


class Habit(Base):
    __tablename__ = "habits"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )

    # Each habit belongs to one user
    user_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False
    )

    # NEW FIELD → Per-user numbering that restarts at 1 for each user
    user_habit_number = Column(Integer, nullable=False, server_default="1")
    # Relationship back to User model
    user = relationship("User", back_populates="habits")

    # One habit → many logs
    logs = relationship(
        "HabitLog",
        back_populates="habit",
        cascade="all, delete-orphan",
        passive_deletes=True
    )
