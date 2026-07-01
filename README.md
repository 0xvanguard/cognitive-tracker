# 🧠 Cognitive Tracker

> Personal cognitive performance tracker — measure, analyze, and improve your IQ, memory, logic, and focus every day.

![Python](https://img.shields.io/badge/Python-3.11+-blue?logo=python) ![FastAPI](https://img.shields.io/badge/FastAPI-0.110+-green?logo=fastapi) ![Streamlit](https://img.shields.io/badge/Streamlit-1.33+-red?logo=streamlit) ![License](https://img.shields.io/badge/License-MIT-yellow)

---

## 🎯 What is this?

A **local-first, privacy-respecting** CLI + web dashboard to:
- Run scientifically-grounded cognitive tests (logic, memory, arithmetic, attention)
- Track your results over time in a local SQLite database
- Visualize your progress with interactive charts
- Get personalized AI coaching recommendations (via Groq API — free tier)

---

## 📁 Project Structure

```
cognitive-tracker/
├── main.py                  # CLI entry point
├── requirements.txt
├── Dockerfile
├── .env.example
├── tests/
│   ├── logic_test.py        # Pattern matrix reasoning
│   ├── memory_test.py       # Working memory
│   └── arithmetic_test.py   # Speed arithmetic
├── tracker/
│   ├── session.py           # SQLite session recording
│   └── models.py            # Data models
├── analytics/
│   └── charts.py            # Plotly progress charts
├── ai_coach/
│   └── coach.py             # LLM-powered recommendations (Groq)
├── dashboard/
│   └── app.py               # Streamlit dashboard
└── .github/
    └── workflows/
        └── ci.yml           # GitHub Actions: lint + test
```

---

## 🚀 Quick Start

```bash
# 1. Clone and install
git clone https://github.com/0xvanguard/cognitive-tracker.git
cd cognitive-tracker
pip install -r requirements.txt

# 2. Configure (optional — for AI coach)
cp .env.example .env
# Add your GROQ_API_KEY in .env (free at console.groq.com)

# 3. Run a session
python main.py

# 4. Launch dashboard
streamlit run dashboard/app.py
```

---

## 🧪 Cognitive Tests

| Test | Measures | Duration |
|------|----------|----------|
| Logic / Pattern Matrix | Fluid intelligence, reasoning | ~3 min |
| Working Memory | Short-term retention, focus | ~2 min |
| Speed Arithmetic | Processing speed, mental agility | ~2 min |

---

## 🤖 AI Coach

Uses **Groq** (Llama 3 — free tier) to analyze your session history and generate:
- Weekly performance summaries
- Specific weak-area recommendations
- Custom daily training plans

Get your free API key at [console.groq.com](https://console.groq.com)

---

## 🛡️ Privacy

All data stays **100% local** on your machine. No data sent to any third party unless you explicitly use the AI coach feature.

---

## 📄 License

MIT — built by [@0xvanguard](https://github.com/0xvanguard)
