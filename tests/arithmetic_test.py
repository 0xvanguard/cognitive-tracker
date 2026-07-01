"""Speed Arithmetic test — processing speed and mental agility."""
import time
import random
import operator
from tracker.session import save_session

OPS = {
    "+": operator.add,
    "-": operator.sub,
    "×": operator.mul,
}


def run_arithmetic_test():
    print("\n🔴 SPEED ARITHMETIC TEST")
    print("Solve 10 operations as fast as possible.\n")

    correct = 0
    total = 10
    start = time.time()

    for i in range(1, total + 1):
        op_symbol, op_fn = random.choice(list(OPS.items()))
        if op_symbol == "×":
            a, b = random.randint(2, 12), random.randint(2, 12)
        else:
            a, b = random.randint(10, 99), random.randint(1, 49)
        expected = op_fn(a, b)
        ans = input(f"  Q{i:02d}: {a} {op_symbol} {b} = ").strip()
        try:
            if int(ans) == expected:
                print("  ✅")
                correct += 1
            else:
                print(f"  ❌ Answer was {expected}")
        except ValueError:
            print(f"  ❌ Answer was {expected}")

    duration = time.time() - start
    score = (correct / total) * 100
    mood = input("How do you feel? (great/good/neutral/tired/bad): ").strip() or "neutral"
    save_session("arithmetic", score, correct, total, duration, mood)
    print(f"\n📊 Arithmetic Score: {score:.0f}/100 ({correct}/{total}) in {duration:.1f}s\n")
