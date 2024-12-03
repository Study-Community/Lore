# Global variable for transaction history
transaction_history = []

def show_balance(balance):
    #Displays the current balance.
    print(f"Your balance is ${balance:.2f}")
    print("Transaction History:")
    for transaction in transaction_history:
        print(transaction)

def deposit(balance):
    #Handles depositing money.
    amount = float(input("Enter an amount to be deposited: "))
    if amount < 0:
        print("That's not a valid amount")
        return balance
    else:
        balance += amount
        transaction_history.append(f"Deposited: ${amount:.2f}")
        return balance

def withdraw(balance):
    #Handles withdrawing money.
    amount = float(input("Enter amount to be withdrawn: "))
    if amount > balance:
        print("Insufficient funds")
        return balance
    elif amount < 0:
        print("Amount must be greater than 0")
        return balance
    else:
        balance -= amount
        transaction_history.append(f"Withdrew: ${amount:.2f}")
        return balance

def verify_pin():
    #Prompts the user to enter the PIN code.
    pin = "1234"  # For simplicity, we'll hardcode the PIN (can be stored securely in real apps)
    attempts = 3  # Number of attempts allowed
   
    while attempts > 0:
        entered_pin = input("Enter your PIN: ")
        if entered_pin == pin:
            return True
        else:
            attempts -= 1
            print(f"Incorrect PIN. You have {attempts} attempts left.")
   
    print("Too many incorrect attempts. Exiting.")
    return False

def display_menu():
    #Displays the banking menu.
    print("\n   Northeastern Banking   ")
    print("1. Show Balance")
    print("2. Deposit")
    print("3. Withdraw")
    print("4. Exit")
    print("5. Show Transaction History")

def main():
    #Main function to drive the banking program.
    balance = 0
    is_running = True
   
    if not verify_pin():
        return  # Exit the program if PIN verification fails

    while is_running:
        display_menu()
        choice = input("Enter your choice (1-5): ")

        if choice == '1':
            show_balance(balance)
        elif choice == '2':
            balance = deposit(balance)
        elif choice == '3':
            balance = withdraw(balance)
        elif choice == '4':
            is_running = False
        elif choice == '5':
            show_balance(balance)
        else:
            print("That is not a valid choice.")

    print("Thank you! Have a nice day!")

if __name__ == '__main__':
    main()  