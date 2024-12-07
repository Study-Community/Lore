import requests

def display_main_menu():
    print("\n   Multifunctional System   ")
    print("1. Banking")
    print("2. Currency Converter")
    print("3. Loan Calculator")
    print("4. Stock Market")
    print("5. Exit")

def banking(balance):
    print("\nBanking System")
    print("1. Show Balance")
    print("2. Deposit")
    print("3. Withdraw")
    print("4. Back to Main Menu")
    choice = input("Enter your choice: ")
    if choice == '1':
        print(f"Your balance is ${balance}")
    elif choice == '2':
        amount = float(input("Enter amount to deposit: "))
        balance += amount
        print(f"Deposited ${amount}. New balance is ${balance}")
    elif choice == '3':
        amount = float(input("Enter amount to withdraw: "))
        if amount > balance:
            print("Insufficient funds")
        else:
            balance -= amount
            print(f"Withdrew ${amount}. New balance is ${balance}")
    return balance

def currency_converter():
    # Placeholder for currency converter function
    pass

def loan_calculator():
    # Placeholder for loan calculator function
    pass

def stock_market():
    # Placeholder for stock market function
    pass

def main():
    balance = 0.0
    while True:
        display_main_menu()
        choice = input("Enter your choice: ")
        if choice == '1':
            balance = banking(balance)
        elif choice == '2':
            currency_converter()
        elif choice == '3':
            loan_calculator()
        elif choice == '4':
            stock_market()
        elif choice == '5':
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()