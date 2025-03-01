import requests
from bs4 import BeautifulSoup
from datetime import datetime

class NHLScraper:
    def __init__(self):
        self.base_url = "https://www.espn.com/nhl/"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }

    def getDateString(self):
        today = datetime.now()
        return today.strftime("%Y%m%d"), today.strftime("%B %d, %Y")

    # Fetch HTML conent based on the given endpoint
    def fetchPage(self, endpoint):
        url = f"{self.base_url}{endpoint}"
        response = requests.get(url, headers=self.headers)
        if response.status_code != 200:
            print(f"Failed to retrieve page: {response.status_code}")
            return None
        return BeautifulSoup(response.content, "html.parser")

    # Must be overwritten by subclasses 
    def scrape(self):
        raise NotImplementedError("Subclasses must implement scrape()")