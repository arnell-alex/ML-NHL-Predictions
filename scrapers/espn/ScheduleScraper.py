from scrapers.espn.NHLScraper import NHLScraper

class ScheduleScraper(NHLScraper):
    def __init__(self):
        super().__init__()
        self.games = []

    def scrape(self):
        date_str, display_date = self.getDateString()
        soup_data = self.fetchPage(f"schedule/_/date/{date_str}")
        if soup_data:
            self.parseSchedule(soup_data)
        return display_date

    # Parse HTML for schedule
    def parseSchedule(self, soup_data):
        schedule_table = soup_data.find("div", class_="Table__Scroller")
        if not schedule_table:
            print("No schedule found.")
            return
        
        games = schedule_table.find_all("tr", class_="Table__TR")
        for game in games:
            if "Table__header" in game.get("class", []):
                continue
            teams = game.find_all("td", class_="Table__TD")
            if len(teams) >= 3:
                self.games.append({
                    "away_team": teams[0].text.strip(),
                    "home_team": teams[1].text.strip(),
                    "time": teams[2].text.strip()
                })

    def printData(self):
        display_date = self.getDateString()[1]
        if not self.games:
            print("No games to display.")
            return
        print(f"NHL Schedule for {display_date}:")
        print("-" * 50)
        for game in self.games:
            print(f"{game['away_team']} @ {game['home_team']} - {game['time']}")
        print("-" * 50)

if __name__ == "__main__":
    scraper = ScheduleScraper()
    scraper.scrape()
    scraper.printData()