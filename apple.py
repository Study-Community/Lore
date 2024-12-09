#demo code 

import requests

transaction_history = []

"""Bank"""

def show_balance(balance):
    """Displays the current balance."""
    print(f"Your balance is ${balance:.2f}")
    print("Transaction History:")
    for transaction in transaction_history:
        print(transaction)

def deposit(balance):
    """Handles depositing money."""
    amount = float(input("Enter an amount to be deposited: "))
    if amount < 0:
        print("That's not a valid amount.")
        return balance
    else:
        balance += amount
        transaction_history.append(f"Deposited: ${amount:.2f}")
        return balance

def withdraw(balance):
    """Handles withdrawing money."""
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
    pin = "1234"  
    attempts = 3
   
    while attempts > 0:
        entered_pin = input("Enter your PIN: ")
        if entered_pin == pin:
            return True
        else:
            attempts -= 1
            print(f"Incorrect PIN. You have {attempts} attempts left.")
   
    print("Too many incorrect attempts. Exiting.")
    return False

def display_banking_menu():
    """Displays the banking menu."""
    print("\n   Banking Program   ")
    print("a. Show Balance")
    print("b. Deposit")
    print("c. Withdraw")
    print("d. Exit")
    print("e. Show Transaction History")

"""Currency Converter"""

class CurrencyConverter:
    def __init__(self):
        self.rates = {
            'USD': 1,
            'EUR': 0.92,
            'GBP': 0.81,
            'INR': 74.27,
            'CNY': 7.29  
        }

    def convert(self, amount, from_currency, to_currency):
        if from_currency == to_currency:
            return amount
        if from_currency not in self.rates or to_currency not in self.rates:
            print("Invalid currency.")
            return None
        base_amount = amount / self.rates[from_currency]  
        return base_amount * self.rates[to_currency]  

def currency_conversion():
    """Prompts user for currency conversion."""
    print("\nCurrency Converter")
    amount = float(input("Enter amount: "))
    from_currency = input("Enter the currency to convert from (USD, EUR, GBP, INR, CNY): ").upper()
    to_currency = input("Enter the currency to convert to (USD, EUR, GBP, INR, CNY): ").upper()

    converter = CurrencyConverter()
    result = converter.convert(amount, from_currency, to_currency)

    if result is not None:
        print(f"{amount} {from_currency} is equal to {result:.2f} {to_currency}")
    else:
        print("Conversion Error.")

"""Loan"""

class LoanEMICalculator:
    def __init__(self, principal, annual_rate, tenure_years):
        self.principal = principal
        self.annual_rate = annual_rate
        self.tenure_years = tenure_years

    def calculate_emi(self):
        """Calculates and returns the EMI."""
        monthly_rate = self.annual_rate / 12 / 100  
        number_of_months = self.tenure_years * 12  

        emi = (self.principal * monthly_rate * (1 + monthly_rate) ** number_of_months) / ((1 + monthly_rate) ** number_of_months - 1)
        return emi

    def calculate_total_payment(self):
        """Calculates total payment over the entire loan tenure."""
        emi = self.calculate_emi()
        total_payment = emi * self.tenure_years * 12  
        return total_payment

    def display_details(self):
        """Displays the loan details and calculated EMI."""
        emi = self.calculate_emi()
        total_payment = self.calculate_total_payment()
       
        print(f"Loan Details:")
        print(f"Principal Amount: ${self.principal}")
        print(f"Annual Interest Rate: {self.annual_rate}%")
        print(f"Loan Tenure: {self.tenure_years} years")
        print(f"Monthly EMI: ${emi:.2f}")
        print(f"Total Payment Over {self.tenure_years} years: ${total_payment:.2f}")

def emi_calculator():
    """Prompts user for loan details and calculates the EMI."""
    print("\nEMI Loan Calculator")
    principal = float(input("Enter the loan amount ($): "))
    annual_rate = float(input("Enter the annual interest rate (in %): "))
    tenure_years = int(input("Enter the loan tenure (in years): "))

    loan_calculator = LoanEMICalculator(principal, annual_rate, tenure_years)
    loan_calculator.display_details()

"""Stock"""

API_KEY_STOCK = 'EQZ0DD6Z647Z1GFS'
BASE_URL_STOCK = 'https://www.alphavantage.co/query'

def get_stock_data(symbol):
    """Fetches real-time stock data for the given symbol."""
    params = {
        'function': 'TIME_SERIES_INTRADAY',
        'symbol': symbol,                    
        'interval': '5min',                
        'apikey': API_KEY_STOCK            
    }

    response = requests.get(BASE_URL_STOCK, params=params)
   
    if response.status_code == 200:  
        data = response.json()

        if f"Time Series (5min)" in data:
            print(f"\nReal-time Stock Data for {symbol}:")
            time_series = data[f'Time Series (5min)']
            latest_time = list(time_series.keys())[0]  
            latest_data = time_series[latest_time]
           
            print(f"Time: {latest_time}")
            print(f"Open: {latest_data['1. open']}")
            print(f"High: {latest_data['2. high']}")
            print(f"Low: {latest_data['3. low']}")
            print(f"Close: {latest_data['4. close']}")
            print(f"Volume: {latest_data['5. volume']}")
        else:
            print("Error101.")

"""Return on Investment"""

def calculate_compound_interest(principal, annual_rate, times_per_year, years):
    """Calculates compound interest."""
    rate = annual_rate / 100
    amount = principal * (1 + rate / times_per_year) ** (times_per_year * years)
    return amount

def compound_interest_calculator():
    """Prompts user for compound interest calculation."""
    print("\nCompound Interest Calculator")
    principal = float(input("Enter the principal investment amount ($): "))
    annual_rate = float(input("Enter the annual interest rate (%): "))
    times_per_year = int(input("Enter the number of times interest is compounded per year: "))
    years = int(input("Enter the number of years the money is invested for: "))

    final_amount = calculate_compound_interest(principal, annual_rate, times_per_year, years)

    print(f"\nInvestment Details:")
    print(f"Principal: ${principal:,.2f}")
    print(f"Annual Interest Rate: {annual_rate}%")
    print(f"Compounding Frequency: {times_per_year} times per year")
    print(f"Investment Duration: {years} years")
    print(f"Final Amount: ${final_amount:,.2f}")

"""Main Menu"""

def display_main_menu():
    print("\n   Finance System   ")
    print("a. Bank")
    print("b. Currency Converter")
    print("c. Loan Payment")
    print("d. Stock Market")
    print("e. Investment Return")
    print("f. Exit")

def main():
    balance = 0
    is_running = True
    while is_running:
        display_main_menu()
        choice = input("Enter your choice (a-f): ")

        if choice == 'a':
            if not verify_pin():
                continue  
            is_banking = True
            while is_banking:
                display_banking_menu()
                banking_choice = input("Enter your choice (a-f): ")

                if banking_choice == 'a':
                    show_balance(balance)
                elif banking_choice == 'b':
                    balance = deposit(balance)
                elif banking_choice == 'c':
                    balance = withdraw(balance)
                elif banking_choice == 'd':
                    is_banking = False
                elif banking_choice == 'e':
                    show_balance(balance)
                else:
                    print("Error101.")
       
        elif choice == 'b':
            currency_conversion()
       
        elif choice == 'c':
            emi_calculator()
       
        elif choice == 'd':
            symbol = input("Enter the stock symbol (e.g., AAPL for Apple): ")
            get_stock_data(symbol)
        elif choice == 'e':
            compound_interest_calculator()
        elif choice == 'f':
            print("Thank you! Exiting the Finance System.")
            is_running = False
        else:
            print("Error101.")

if __name__ == "__main__":
    main()