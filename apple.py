import requests

def display_main_menu():
    print("\n   Multifunctional System   ")
    print("1. Banking")
    print("2. Weather App")
    print("3. Currency Converter")
    print("4. EMI Loan Calculator")
    print("5. Stock Market")
    print("6. Exit")

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

def weather_app():
    city = input("Enter city name: ")
    api_key = 'your_api_key_here'
    url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=imperial'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        print(f"\nWeather in {data['name']}, {data['sys']['country']}:")
        print(f"Temperature: {data['main']['temp']}°F")
        print(f"Weather: {data['weather'][0]['description']}")
        print(f"Humidity: {data['main']['humidity']}%")
        print(f"Wind Speed: {data['wind']['speed']} m/s")
    else:
        print("Error fetching weather data")

def currency_converter():
    amount = float(input("Enter amount: "))
    from_currency = input("From currency (e.g., USD): ")
    to_currency = input("To currency (e.g., EUR): ")
    rates = {'USD': 1, 'EUR': 0.92, 'GBP': 0.81, 'INR': 74.27, 'CNY': 7.29}
    if from_currency in rates and to_currency in rates:
        converted_amount = amount / rates[from_currency] * rates[to_currency]
        print(f"{amount} {from_currency} is equal to {converted_amount} {to_currency}")
    else:
        print("Invalid currency")

def emi_calculator():
    principal = float(input("Enter loan amount: "))
    annual_rate = float(input("Enter annual interest rate (%): "))
    tenure_years = int(input("Enter loan tenure (years): "))
    monthly_rate = annual_rate / 12 / 100
    number_of_months = tenure_years * 12
    emi = (principal * monthly_rate * (1 + monthly_rate) ** number_of_months) / ((1 + monthly_rate) ** number_of_months - 1)
    total_payment = emi * number_of_months
    print(f"Monthly EMI: ${emi}")
    print(f"Total Payment: ${total_payment}")

def stock_market():
    symbol = input("Enter stock symbol (e.g., AAPL): ")
    api_key = 'your_api_key_here'
    url = f'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol={symbol}&interval=5min&apikey={api_key}'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if 'Time Series (5min)' in data:
            latest_time = list(data['Time Series (5min)'].keys())[0]
            latest_data = data['Time Series (5min)'][latest_time]
            print(f"\nReal-time Stock Data for {symbol}:")
            print(f"Time: {latest_time}")
            print(f"Open: {latest_data['1. open']}")
            print(f"High: {latest_data['2. high']}")
            print(f"Low: {latest_data['3. low']}")
            print(f"Close: {latest_data['4. close']}")
            print(f"Volume: {latest_data['5. volume']}")
        else:
            print("Error fetching stock data")
    else:
        print("Error fetching stock data")

def main():
    balance = 0
    is_running = True
    while is_running:
        display_main_menu()
        choice = input("Enter your choice (1-6): ")
        if choice == '1':
            balance = banking(balance)
        elif choice == '2':
            weather_app()
        elif choice == '3':
            currency_converter()
        elif choice == '4':
            emi_calculator()
        elif choice == '5':
            stock_market()
        elif choice == '6':
            is_running = False
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()