import requests

# Använd Tor-proxyn
proxies = {
    'http': 'socks5h://127.0.0.1:9050',
    'https': 'socks5h://127.0.0.1:9050'
}

def check_ip():
    """Kollar vilken IP-adress AI:n har genom Tor."""
    url = "http://check.torproject.org/api/ip"
    try:
        response = requests.get(url, proxies=proxies)
        print(f"🔍 AI:s nuvarande IP-adress: {response.text}")
    except Exception as e:
        print(f"⚠️ Fel vid anslutning till Tor: {e}")

check_ip()
