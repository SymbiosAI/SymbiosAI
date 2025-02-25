import requests
from bs4 import BeautifulSoup
import json
import os

# Använd Tor-proxyn för anonymitet
proxies = {
    'http': 'socks5h://127.0.0.1:9050',
    'https': 'socks5h://127.0.0.1:9050'
}

# Använd en riktig webbläsares User-Agent för att undvika blockering
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
    'Accept-Language': 'en-US,en;q=0.9',
    'Referer': 'https://www.google.com/',
    'DNT': '1',  # Do Not Track
    'Upgrade-Insecure-Requests': '1'
}

# Skapa en mapp för lagring av insamlad data
data_dir = "/SymbiosAI/data"
if not os.path.exists(data_dir):
    os.makedirs(data_dir)

def scrape_page(url):
    """Hämtar och analyserar en webbsida, vissa sidor körs utan Tor"""
    try:
        session = requests.Session()
        session.headers.update(headers)

        # Om det är Reuters, använd direkt anslutning istället för Tor
        if "reuters.com" in url:
            response = session.get(url, timeout=10)
        else:
            session.proxies = proxies
            response = session.get(url, timeout=10)

        response.raise_for_status()  # Kastar fel om sidan inte laddas

        soup = BeautifulSoup(response.text, 'html.parser')
        title = soup.title.string if soup.title else "Ingen titel hittad"
        text = ' '.join([p.text for p in soup.find_all('p')])  # Hämtar textinnehåll
        links = [a['href'] for a in soup.find_all('a', href=True) if a['href'].startswith("http")]

        page_data = {
            "url": url,
            "title": title,
            "text": text[:500],  # Begränsar till 500 tecken för lagring
            "links": links[:5]   # Begränsar till 5 länkar för analys
        }

        filename = f"{data_dir}/{url.replace('http://', '').replace('https://', '').replace('/', '_')}.json"
        with open(filename, "w", encoding="utf-8") as file:
            json.dump(page_data, file, indent=4, ensure_ascii=False)

        print(f"✅ Sparade data från: {url}")
        return page_data

    except requests.exceptions.RequestException as e:
        print(f"⚠️ Fel vid hämtning av {url}: {e}")
        return None

# Lista av sidor att besöka
urls = [
    "http://check.torproject.org",
    "https://www.bbc.com",
    "https://www.cnbc.com/world",
    "https://www.reuters.com"
]

# Besök och analysera varje sida
for url in urls:
    scrape_page(url)


