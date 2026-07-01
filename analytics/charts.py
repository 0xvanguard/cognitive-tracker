"""Generate Plotly charts from session history."""
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from tracker.session import get_all_sessions


def load_dataframe() -> pd.DataFrame:
    sessions = get_all_sessions()
    if not sessions:
        return pd.DataFrame()
    df = pd.DataFrame(sessions)
    df["created_at"] = pd.to_datetime(df["created_at"])
    df["date"] = df["created_at"].dt.date
    return df


def plot_score_over_time():
    """Line chart of scores per test type over time."""
    df = load_dataframe()
    if df.empty:
        print("No data yet. Run some tests first!")
        return
    fig = px.line(
        df,
        x="created_at",
        y="score",
        color="test_type",
        markers=True,
        title="Cognitive Score Over Time",
        labels={"score": "Score (0-100)", "created_at": "Date", "test_type": "Test"},
    )
    fig.update_layout(template="plotly_dark", legend_title="Test Type")
    fig.show()


def plot_radar_latest():
    """Radar chart of latest scores per test type."""
    df = load_dataframe()
    if df.empty:
        return
    latest = df.sort_values("created_at").groupby("test_type")["score"].last().reset_index()
    fig = go.Figure(
        go.Scatterpolar(
            r=latest["score"],
            theta=latest["test_type"],
            fill="toself",
            name="Latest Score",
        )
    )
    fig.update_layout(
        polar=dict(radialaxis=dict(visible=True, range=[0, 100])),
        title="Latest Cognitive Profile",
        template="plotly_dark",
    )
    fig.show()


def plot_weak_areas():
    """Bar chart showing average score per test to identify weak areas."""
    df = load_dataframe()
    if df.empty:
        return
    avg = df.groupby("test_type")["score"].mean().reset_index()
    avg.columns = ["Test", "Average Score"]
    colors = ["#e74c3c" if s < 60 else "#f39c12" if s < 80 else "#2ecc71"
              for s in avg["Average Score"]]
    fig = px.bar(
        avg,
        x="Test",
        y="Average Score",
        title="Average Score by Test (Weak Area Identifier)",
        color="Test",
        color_discrete_sequence=colors,
        text_auto=".1f",
    )
    fig.update_layout(template="plotly_dark", showlegend=False)
    fig.add_hline(y=60, line_dash="dash", line_color="red", annotation_text="Threshold 60")
    fig.show()
