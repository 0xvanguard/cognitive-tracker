"""Unit tests for tracker models and session utilities."""
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from tracker.models import Base, Session as CogSession


@pytest.fixture
def test_db():
    """In-memory SQLite database for testing."""
    engine = create_engine("sqlite:///:memory:", echo=False)
    Base.metadata.create_all(engine)
    TestSession = sessionmaker(bind=engine)
    db = TestSession()
    yield db
    db.close()


def test_create_session(test_db):
    record = CogSession(
        test_type="logic",
        score=80.0,
        raw_correct=4,
        raw_total=5,
        duration_seconds=120.0,
        mood="good",
    )
    test_db.add(record)
    test_db.commit()
    result = test_db.query(CogSession).first()
    assert result is not None
    assert result.test_type == "logic"
    assert result.score == 80.0
    assert result.raw_correct == 4


def test_score_range(test_db):
    """Score must be between 0 and 100."""
    for score in [0.0, 50.0, 100.0]:
        record = CogSession(
            test_type="memory",
            score=score,
            raw_correct=1,
            raw_total=1,
            duration_seconds=10.0,
        )
        test_db.add(record)
    test_db.commit()
    results = test_db.query(CogSession).all()
    scores = [r.score for r in results]
    assert all(0 <= s <= 100 for s in scores)


def test_mood_default(test_db):
    record = CogSession(test_type="arithmetic", score=70.0, raw_correct=7, raw_total=10,
                        duration_seconds=60.0)
    test_db.add(record)
    test_db.commit()
    result = test_db.query(CogSession).filter_by(test_type="arithmetic").first()
    assert result.mood == "neutral"
