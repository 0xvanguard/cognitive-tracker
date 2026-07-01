"""cognitive-tracker — CLI entry point."""
import sys
from tracker.session import init_db
from tests.logic_test import run_logic_test
from tests.memory_test import run_memory_test
from tests.arithmetic_test import run_arithmetic_test
from ai_coach.coach import get_recommendations


MENU = """
╔══════════════════════════════════╗
║    🧠  COGNITIVE TRACKER         ║
╠══════════════════════════════════╣
║  1. Logic / Pattern Matrix       ║
║  2. Working Memory               ║
║  3. Speed Arithmetic             ║
║  4. Full Session (all 3 tests)   ║
║  5. Get AI Coach Recommendations ║
║  6. Exit                         ║
╚══════════════════════════════════╝
"""


def main():
    init_db()
    while True:
        print(MENU)
        choice = input("Select an option (1-6): ").strip()
        if choice == "1":
            run_logic_test()
        elif choice == "2":
            run_memory_test()
        elif choice == "3":
            run_arithmetic_test()
        elif choice == "4":
            print("\n--- Starting Full Session ---")
            run_logic_test()
            run_memory_test()
            run_arithmetic_test()
            print("\n✅ Full session complete!")
        elif choice == "5":
            get_recommendations()
        elif choice == "6":
            print("Goodbye! Keep training your brain. 🧠")
            sys.exit(0)
        else:
            print("Invalid option. Try again.")


if __name__ == "__main__":
    main()
