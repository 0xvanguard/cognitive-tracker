"""Database initialization and session recording."""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from tracker.models import Base, Session as CogSession

DB_PATH = "cognitive_data.db"
ENGINE = create_engine(f"sqlite:///{DB_PATH}", echo=False)
SessionLocal = sessionmaker(bind=ENGINE)


def init_db():
    """Create tables if they don't exist."""
    Base.metadata.create_all(ENGINE)
    print(f"📦 Database ready: {DB_PATH}")


def save_session(test_type: str, score: float, correct: int, total: int,
                 duration: float, mood: str = "neutral", notes: str = ""):
    """Save a completed test session."""
    db = SessionLocal()
    try:
        record = CogSession(
            test_type=test_type,
            score=score,
            raw_correct=correct,
            raw_total=total,
            duration_seconds=duration,
            mood=mood,
            notes=notes,
        )
        db.add(record)
        db.commit()
        print(f"✅ Session saved — {test_type} | Score: {score:.1f}/100")
    finally:
        db.close()


def get_all_sessions() -> list:
    """Return all sessions as a list of dicts."""
    db = SessionLocal()
    try:
        records = db.query(CogSession).order_by(CogSession.created_at).all()
        return [
            {
                "id": r.id,
                "test_type": r.test_type,
                "score": r.score,
                "raw_correct": r.raw_correct,
                "raw_total": r.raw_total,
                "duration_seconds": r.duration_seconds,
                "mood": r.mood,
                "notes": r.notes,
                "created_at": r.created_at.isoformat(),
            }
            for r in records
        ]
    finally:
        db.close()
