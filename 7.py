import requests

def convert_currency(amount, from_currency, to_currency):
    url = f"https://api.exchangerate-api.com/v4/latest/{from_currency}"
    response = requests.get(url).json()
    rate = response["rates"].get(to_currency)
    if rate:
        print(f"{amount} {from_currency} = {amount * rate:.2f} {to_currency}")
    else:
        print(f"Conversion rate not available for {to_currency}.")

if __name__ == "__main__":
    amount = float(input("Enter amount: "))
    from_currency = input("From currency (e.g., USD): ").upper()
    to_currency = input("To currency (e.g., EUR): ").upper()
    convert_currency(amount, from_currency, to_currency)