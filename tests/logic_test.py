"""Logic / Pattern Matrix test — measures fluid reasoning."""
import time
import random
from tracker.session import save_session

QUESTIONS = [
    {
        "q": "2, 4, 8, 16, ?",
        "options": ["24", "32", "30", "20"],
        "answer": "32",
        "explanation": "Each number doubles.",
    },
    {
        "q": "1, 4, 9, 16, ?",
        "options": ["20", "25", "24", "36"],
        "answer": "25",
        "explanation": "Perfect squares: 1², 2², 3², 4², 5².",
    },
    {
        "q": "3, 6, 11, 18, ?",
        "options": ["25", "27", "29", "23"],
        "answer": "27",
        "explanation": "Differences: +3, +5, +7, +9.",
    },
    {
        "q": "Odd one out: Dog, Cat, Eagle, Fish",
        "options": ["Dog", "Cat", "Eagle", "Fish"],
        "answer": "Eagle",
        "explanation": "Eagle is a bird; others are mammals or aquatic.",
    },
    {
        "q": "If all Bloops are Razzles, and all Razzles are Lazzles, are all Bloops Lazzles?",
        "options": ["Yes", "No", "Maybe", "Impossible to tell"],
        "answer": "Yes",
        "explanation": "Transitive logic.",
    },
    {
        "q": "100, 50, 25, 12.5, ?",
        "options": ["6", "6.25", "5", "8"],
        "answer": "6.25",
        "explanation": "Each divided by 2.",
    },
    {
        "q": "Which shape has the most sides: hexagon, pentagon, octagon, heptagon?",
        "options": ["Hexagon", "Pentagon", "Octagon", "Heptagon"],
        "answer": "Octagon",
        "explanation": "Octagon = 8 sides.",
    },
    {
        "q": "Mirror of CLOCK is:",
        "options": ["КCOLK", "KCOLD", "KCOLC", "KOЛCK"],
        "answer": "KCOLC",
        "explanation": "Mirror reversal of letters.",
    },
]


def run_logic_test():
    print("\n🔷 LOGIC / PATTERN MATRIX TEST")
    print("Answer as quickly and accurately as possible.\n")
    questions = random.sample(QUESTIONS, min(5, len(QUESTIONS)))
    correct = 0
    start = time.time()

    for i, q in enumerate(questions, 1):
        print(f"Q{i}: {q['q']}")
        for j, opt in enumerate(q["options"], 1):
            print(f"  {j}. {opt}")
        ans_idx = input("Your answer (1-4): ").strip()
        try:
            chosen = q["options"][int(ans_idx) - 1]
        except (IndexError, ValueError):
            chosen = ""
        if chosen == q["answer"]:
            print("  ✅ Correct!")
            correct += 1
        else:
            print(f"  ❌ Incorrect. Answer: {q['answer']} — {q['explanation']}")
        print()

    duration = time.time() - start
    score = (correct / len(questions)) * 100
    mood = input("How do you feel? (great/good/neutral/tired/bad): ").strip() or "neutral"
    save_session("logic", score, correct, len(questions), duration, mood)
    print(f"\n📊 Logic Score: {score:.0f}/100 ({correct}/{len(questions)}) in {duration:.1f}s\n")
