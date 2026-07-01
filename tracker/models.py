"""SQLAlchemy models for cognitive sessions."""
from datetime import datetime
from sqlalchemy import Column, Integer, Float, String, DateTime
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class Session(Base):
    __tablename__ = "sessions"

    id = Column(Integer, primary_key=True, autoincrement=True)
    test_type = Column(String, nullable=False)  # logic | memory | arithmetic
    score = Column(Float, nullable=False)        # 0–100 normalized
    raw_correct = Column(Integer, default=0)
    raw_total = Column(Integer, default=0)
    duration_seconds = Column(Float, default=0.0)
    mood = Column(String, default="neutral")     # great | good | neutral | tired | bad
    notes = Column(String, default="")
    created_at = Column(DateTime, default=datetime.utcnow)

    def __repr__(self):
        return (
            f"<Session id={self.id} type={self.test_type} "
            f"score={self.score:.1f} at={self.created_at.date()}>"
        )
