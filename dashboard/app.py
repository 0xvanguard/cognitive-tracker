"""Streamlit dashboard for cognitive performance tracking."""
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from tracker.session import get_all_sessions, init_db

st.set_page_config(
    page_title="Cognitive Tracker",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded",
)

init_db()

# Sidebar
st.sidebar.title("🧠 Cognitive Tracker")
st.sidebar.markdown("Track · Analyze · Improve")
page = st.sidebar.radio("Navigate", ["📊 Dashboard", "📅 History", "🤖 AI Coach"])


def load_data() -> pd.DataFrame:
    sessions = get_all_sessions()
    if not sessions:
        return pd.DataFrame()
    df = pd.DataFrame(sessions)
    df["created_at"] = pd.to_datetime(df["created_at"])
    df["date"] = df["created_at"].dt.date
    return df


df = load_data()

# ── Dashboard Page ──────────────────────────────────────────────────────
if page == "📊 Dashboard":
    st.title("📊 Cognitive Performance Dashboard")

    if df.empty:
        st.info("No data yet! Run `python main.py` in your terminal to record sessions.")
    else:
        # KPI row
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Sessions", len(df))
        with col2:
            latest_score = df.sort_values("created_at").iloc[-1]["score"]
            st.metric("Last Score", f"{latest_score:.0f}/100")
        with col3:
            overall_avg = df["score"].mean()
            st.metric("Overall Average", f"{overall_avg:.1f}/100")
        with col4:
            weak = df.groupby("test_type")["score"].mean().idxmin()
            st.metric("Weakest Area", weak.capitalize())

        st.divider()

        # Score over time
        fig_line = px.line(
            df,
            x="created_at",
            y="score",
            color="test_type",
            markers=True,
            title="Score Over Time by Test",
        )
        st.plotly_chart(fig_line, use_container_width=True)

        col_left, col_right = st.columns(2)

        with col_left:
            # Radar of latest scores
            latest = df.sort_values("created_at").groupby("test_type")["score"].last().reset_index()
            fig_radar = go.Figure(
                go.Scatterpolar(
                    r=latest["score"],
                    theta=latest["test_type"],
                    fill="toself",
                )
            )
            fig_radar.update_layout(
                polar=dict(radialaxis=dict(range=[0, 100])),
                title="Cognitive Profile (Latest)",
            )
            st.plotly_chart(fig_radar, use_container_width=True)

        with col_right:
            # Weak area bar
            avg_scores = df.groupby("test_type")["score"].mean().reset_index()
            fig_bar = px.bar(
                avg_scores,
                x="test_type",
                y="score",
                title="Average Score per Test",
                text_auto=".1f",
                color="score",
                color_continuous_scale="RdYlGn",
                range_color=[0, 100],
            )
            fig_bar.add_hline(y=60, line_dash="dash", line_color="red")
            st.plotly_chart(fig_bar, use_container_width=True)

# ── History Page ────────────────────────────────────────────────────────
elif page == "📅 History":
    st.title("📅 Session History")
    if df.empty:
        st.info("No sessions recorded yet.")
    else:
        filter_type = st.selectbox("Filter by test type", ["All"] + df["test_type"].unique().tolist())
        if filter_type != "All":
            filtered = df[df["test_type"] == filter_type]
        else:
            filtered = df
        st.dataframe(
            filtered[["created_at", "test_type", "score", "raw_correct",
                       "raw_total", "duration_seconds", "mood"]].sort_values(
                "created_at", ascending=False
            ),
            use_container_width=True,
        )

# ── AI Coach Page ────────────────────────────────────────────────────────
elif page == "🤖 AI Coach":
    st.title("🤖 AI Coach")
    st.markdown("Get personalized recommendations from your AI coach powered by Groq.")

    import os
    from dotenv import load_dotenv
    load_dotenv()
    api_key = os.getenv("GROQ_API_KEY", "")

    if not api_key:
        st.warning(
            "No GROQ_API_KEY found. "
            "[Get a free key at console.groq.com](https://console.groq.com) "
            "and add it to your `.env` file."
        )
    elif df.empty:
        st.info("Run some tests first to get personalized recommendations!")
    else:
        if st.button("🧠 Get Recommendations", type="primary"):
            from ai_coach.coach import get_recommendations
            with st.spinner("Consulting your AI coach..."):
                import io
                import sys
                buf = io.StringIO()
                old_stdout = sys.stdout
                sys.stdout = buf
                get_recommendations()
                sys.stdout = old_stdout
                output = buf.getvalue()
            st.markdown("```\n" + output + "\n```")
