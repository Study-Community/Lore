def add_expense(expenses, amount, category):
    expenses.append({"amount": amount, "category": category})
    print(f"Expense of {amount} in category '{category}' added.")

def view_expenses(expenses):
    total = sum(exp['amount'] for exp in expenses)
    print(f"Total expenses: {total}")
    for i, exp in enumerate(expenses, 1):
        print(f"{i}. {exp['amount']} in {exp['category']}")

if __name__ == "__main__":
    expenses = []
    while True:
        print("\nOptions: [1] Add Expense [2] View Expenses [3] Exit")
        choice = input("Choose an option: ")
        if choice == "1":
            amount = float(input("Enter the amount: "))
            category = input("Enter the category: ")
            add_expense(expenses, amount, category)
        elif choice == "2":
            view_expenses(expenses)
        elif choice == "3":
            print("Goodbye!")
            break
        else:
            print("Invalid option.")