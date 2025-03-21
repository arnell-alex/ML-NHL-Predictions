# nhl_scraper_project/scrapers/fanduel/DraftKingsOddsScraper.py
from scrapers.espn.NHLScraper import NHLScraper
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time
import random

class DraftKingsOddsScraper(NHLScraper):
    def __init__(self):
        """Initialize with a dictionary to store game odds."""
        super().__init__()
        self.game_odds = {}  # Key: game matchup, Value: dict of team odds and total points

    def fetchPage(self, url):
        """Fetch page using Selenium with stealth options."""
        options = Options()
        options.add_argument("--headless")
        options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36")
        options.add_argument("--disable-blink-features=AutomationControlled")
        driver = webdriver.Chrome(options=options)
        driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
            "source": "Object.defineProperty(navigator, 'webdriver', { get: () => undefined })"
        })
        driver.get(url)
        time.sleep(random.uniform(2, 5))  # Random delay
        soup = BeautifulSoup(driver.page_source, "html.parser")
        driver.quit()
        return soup

    def scrapeTonightOdds(self):
        """Scrape odds for tonight's NHL games from DraftKings."""
        url = "https://sportsbook.draftkings.com/leagues/hockey/nhl"
        soup = self.fetchPage(url)
        if soup:
            self.parseOdds(soup)
        else:
            print("Failed to fetch DraftKings NHL odds page")

    def parseOdds(self, soup):
        """Parse spread, moneyline, and total points from sportsbook-table__body."""
        table_body = soup.find("tbody", class_="sportsbook-table__body")
        if not table_body:
            print("No sportsbook-table__body found")
            return

        rows = table_body.find_all("tr")  # Each <tr> is a team
        if len(rows) < 2:
            print("Not enough rows to form matchups")
            return

        today = datetime.now().strftime("%b %d")  # e.g., "Mar 16"
        for i in range(0, len(rows), 2):  # Step by 2 to pair teams
            if i + 1 >= len(rows):  # Ensure we have a pair
                break

            team1_row = rows[i]
            team2_row = rows[i + 1]

            # Extract team names from <th>
            team1_th = team1_row.find("th")
            team2_th = team2_row.find("th")
            if not team1_th or not team2_th:
                print(f"Missing team name <th> for row pair at index {i}")
                continue

            # Extract odds cells from <td class="sportsbook-table__column-row">
            team1_cells = team1_row.find_all("td", class_="sportsbook-table__column-row")
            team2_cells = team2_row.find_all("td", class_="sportsbook-table__column-row")
            if len(team1_cells) < 3 or len(team2_cells) < 3:  # Need at least 3 (Puck Line, Total, Moneyline)
                print(f"Insufficient cells for {team1_th.text.strip()} vs. {team2_th.text.strip()}: {len(team1_cells)}/{len(team2_cells)}")
                continue

            # Team names (strip scores if present)
            team1_name = " ".join(team1_th.text.strip().split()[:2])  # First two words
            team2_name = " ".join(team2_th.text.strip().split()[:2])  # First two words
            matchup = f"{team1_name} vs. {team2_name}"

            # Parse spread (e.g., "-1.5 (-110)" → points: "-1.5", odds: "-110")
            team1_spread_parts = team1_cells[0].text.strip().split()
            team2_spread_parts = team2_cells[0].text.strip().split()
            team1_total_parts = team1_cells[1].text.strip().split()
            team2_total_parts = team2_cells[1].text.strip().split()

            odds = {
                "teams": {
                    team1_name: {
                        "spread": {
                            "points": team1_spread_parts[0],  # e.g., "-1.5"
                            "odds": team1_spread_parts[1] if len(team1_spread_parts) > 1 else "N/A"  # e.g., "(-110)"
                        },
                        "moneyline": team1_cells[2].text.strip()  # e.g., "-150"
                    },
                    team2_name: {
                        "spread": {
                            "points": team2_spread_parts[0],  # e.g., "+1.5"
                            "odds": team2_spread_parts[1] if len(team2_spread_parts) > 1 else "N/A"  # e.g., "(-110)"
                        },
                        "moneyline": team2_cells[2].text.strip()  # e.g., "+130"
                    }
                },
                "total_points": {
                    "over": {
                        "points": team1_total_parts[1],  # e.g., "5.5" (skip "O")
                        "odds": team1_total_parts[2] if len(team1_total_parts) > 2 else "N/A"  # e.g., "(-105)"
                    },
                    "under": {
                        "points": team2_total_parts[1],  # e.g., "5.5" (skip "U")
                        "odds": team2_total_parts[2] if len(team2_total_parts) > 2 else "N/A"  # e.g., "(-115)"
                    }
                }
            }

            self.game_odds[matchup] = odds

        if self.game_odds:
            print(f"Parsed odds for {len(self.game_odds)} games")
        else:
            print("No odds parsed for tonight's games")

    def printOdds(self):
        """Print all scraped game odds."""
        if not self.game_odds:
            print("No game odds to display.")
            return
        print("\nTonight's NHL Game Odds (DraftKings):")
        print("-" * 100)
        print(f"{'Matchup':<30} {'Team':<20} {'Spread':<15} {'Moneyline':<15} {'Total Points':<20}")
        print("-" * 100)
        for matchup, data in self.game_odds.items():
            team1_name = list(data["teams"].keys())[0]
            team2_name = list(data["teams"].keys())[1]
            team1 = data["teams"][team1_name]
            team2 = data["teams"][team2_name]
            spread1 = f"{team1['spread']['points']} {team1['spread']['odds']}"
            spread2 = f"{team2['spread']['points']} {team2['spread']['odds']}"
            total = f"O {data['total_points']['over']['points']} {data['total_points']['over']['odds']} / U {data['total_points']['under']['points']} {data['total_points']['under']['odds']}"
            print(f"{matchup:<30} {team1_name:<20} {spread1:<15} {team1['moneyline']:<15} {total:<20}")
            print(f"{'':<30} {team2_name:<20} {spread2:<15} {team2['moneyline']:<15}")
        print("-" * 100)

    def getGameOdds(self, matchup):
        """Return the odds for a specific game matchup."""
        return self.game_odds.get(matchup, {})

if __name__ == "__main__":
    scraper = DraftKingsOddsScraper()
    scraper.scrapeTonightOdds()
    scraper.printOdds()