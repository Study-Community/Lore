import requests

def get_weather(city):
    api_key = "your_openweathermap_api_key"
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    response = requests.get(url).json()
    if response.get("main"):
        print(f"Weather in {city}: {response['weather'][0]['description']}")
        print(f"Temperature: {response['main']['temp']}°C")
    else:
        print(f"Could not find weather for {city}.")

if __name__ == "__main__":
    city = input("Enter city name: ")
    get_weather(city)