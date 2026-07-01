"""AI Coach powered by Groq (Llama 3 — free tier)."""
import os
import json
from dotenv import load_dotenv
from tracker.session import get_all_sessions

load_dotenv()


def get_recommendations():
    """Generate personalized coaching recommendations using Groq."""
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        print(
            "\n⚠️  No GROQ_API_KEY found in .env\n"
            "Get your free key at https://console.groq.com\n"
            "Add it to .env as: GROQ_API_KEY=your_key_here\n"
        )
        return

    sessions = get_all_sessions()
    if not sessions:
        print("\n📭 No sessions yet. Run some tests first!\n")
        return

    try:
        from groq import Groq  # noqa: PLC0415
    except ImportError:
        print("Install groq: pip install groq")
        return

    # Build summary for the prompt
    from collections import defaultdict
    stats = defaultdict(list)
    for s in sessions:
        stats[s["test_type"]].append(s["score"])

    summary_lines = []
    for test_type, scores in stats.items():
        avg = sum(scores) / len(scores)
        trend = "improving" if len(scores) > 1 and scores[-1] > scores[0] else "flat/declining"
        summary_lines.append(
            f"- {test_type.capitalize()}: avg {avg:.1f}/100, last {scores[-1]:.1f}/100, trend: {trend}"
        )
    summary = "\n".join(summary_lines)

    prompt = (
        f"I am tracking my cognitive performance. Here is my data:\n{summary}\n\n"
        "Based on this, give me:\n"
        "1. A brief analysis of my strengths and weak areas\n"
        "2. Three specific exercises or habits to improve my weakest area\n"
        "3. A motivational message\n"
        "Keep it concise and actionable (max 300 words)."
    )

    client = Groq(api_key=api_key)
    model = os.getenv("GROQ_MODEL", "llama3-8b-8192")

    print("\n🤖 Consulting AI Coach...\n")
    response = client.chat.completions.create(
        messages=[{"role": "user", "content": prompt}],
        model=model,
        max_tokens=512,
    )
    advice = response.choices[0].message.content
    print("━" * 50)
    print("🧠 AI COACH RECOMMENDATIONS")
    print("━" * 50)
    print(advice)
    print("━" * 50 + "\n")
