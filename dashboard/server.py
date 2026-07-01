"""Minimal FastAPI server that serves the HTML dashboard and future API routes."""
from pathlib import Path
from fastapi import FastAPI
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from tracker.session import init_db, get_all_sessions

app = FastAPI(title="Cognitive Tracker API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

DASHBOARD_DIR = Path(__file__).parent


@app.on_event("startup")
def startup():
    init_db()


@app.get("/", include_in_schema=False)
def serve_dashboard():
    """Serve the HTML dashboard at root."""
    return FileResponse(DASHBOARD_DIR / "index.html")


@app.get("/api/sessions")
def api_sessions():
    """Return all recorded sessions as JSON."""
    return JSONResponse(content=get_all_sessions())


@app.get("/api/sessions/{test_type}")
def api_sessions_by_type(test_type: str):
    """Return sessions filtered by test type (logic, memory, arithmetic)."""
    all_s = get_all_sessions()
    filtered = [s for s in all_s if s["test_type"] == test_type]
    return JSONResponse(content=filtered)


@app.get("/api/summary")
def api_summary():
    """Return a quick summary of scores per test type."""
    all_s = get_all_sessions()
    from collections import defaultdict
    stats = defaultdict(list)
    for s in all_s:
        stats[s["test_type"]].append(s["score"])
    summary = {
        t: {
            "count": len(scores),
            "avg": round(sum(scores) / len(scores), 1),
            "last": round(scores[-1], 1),
        }
        for t, scores in stats.items()
    }
    return JSONResponse(content=summary)
