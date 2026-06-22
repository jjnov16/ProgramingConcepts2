"""
Monthly Expense Analyzer
Asks the user for a list of monthly expenses (type and amount), then uses the
reduce method to calculate and display the total, highest, and lowest expense.
"""

from functools import reduce


def get_expenses():
    """Prompt the user for expenses until they choose to stop.

    Returns a list of (type, amount) tuples.
    """
    expenses = []
    print("Enter your monthly expenses. Type 'done' for the expense type to finish.\n")

    while True:
        expense_type = input("Expense type: ").strip()
        if expense_type.lower() == "done":
            break
        if not expense_type:
            print("Please enter a valid expense type.\n")
            continue

        # Keep asking until a valid positive number is entered.
        while True:
            amount_input = input(f"Amount for '{expense_type}': $").strip()
            try:
                amount = float(amount_input)
                if amount < 0:
                    print("Amount cannot be negative. Try again.")
                    continue
                break
            except ValueError:
                print("Please enter a valid number.")

        expenses.append((expense_type, amount))
        print()

    return expenses


def main():
    expenses = get_expenses()

    if not expenses:
        print("\nNo expenses entered. Nothing to analyze.")
        return

    # Use reduce with lambda functions for the three calculations.
    total = reduce(lambda acc, item: acc + item[1], expenses, 0)
    highest = reduce(lambda a, b: a if a[1] >= b[1] else b, expenses)
    lowest = reduce(lambda a, b: a if a[1] <= b[1] else b, expenses)

    print("\n----- Expense Summary -----")
    print(f"Total expense:   ${total:.2f}")
    print(f"Highest expense: {highest[0]} (${highest[1]:.2f})")
    print(f"Lowest expense:  {lowest[0]} (${lowest[1]:.2f})")


if __name__ == "__main__":
    main()