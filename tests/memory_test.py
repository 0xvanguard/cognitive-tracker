"""Working Memory test — digit span and sequence recall."""
import time
import random
from tracker.session import save_session


def run_memory_test():
    print("\n🟢 WORKING MEMORY TEST")
    print("You will see a sequence of numbers. Memorize them, then type them back.\n")

    levels = [4, 5, 6, 7, 8]
    correct = 0
    total = len(levels)
    start = time.time()

    for length in levels:
        sequence = [str(random.randint(0, 9)) for _ in range(length)]
        print(f"  Memorize: {' '.join(sequence)}")
        input("  Press Enter when ready...")
        # Clear screen hint
        print("\n" * 3 + "  🔒 Sequence hidden. Type it now.")
        user_input = input("  Your answer: ").strip().replace(" ", "")
        original = "".join(sequence)
        if user_input == original:
            print("  ✅ Correct!")
            correct += 1
        else:
            print(f"  ❌ Incorrect. Was: {original}")
        print()

    duration = time.time() - start
    score = (correct / total) * 100
    mood = input("How do you feel? (great/good/neutral/tired/bad): ").strip() or "neutral"
    save_session("memory", score, correct, total, duration, mood)
    print(f"\n📊 Memory Score: {score:.0f}/100 ({correct}/{total}) in {duration:.1f}s\n")
