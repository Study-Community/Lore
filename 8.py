import requests
from bs4 import BeautifulSoup

def scrape_page(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    print("Page Title:", soup.title.string)
    print("Links on the page:")
    for link in soup.find_all('a', href=True):
        print(link['href'])

if __name__ == "__main__":
    url = input("Enter a URL: ")
    scrape_page(url)