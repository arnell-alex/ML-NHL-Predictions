from scrapers.espn.NHLScraper import NHLScraper
from data.NHLTeams import NHL_TEAMS, getTeamEndpoint

class RosterScraper(NHLScraper):
    def __init__(self):
        super().__init__()
        # Key: team name, Value: list of {"name": str, "id": str}
        self.team_rosters = {}  

    # Get players for every team
    def scrapeAllTeams(self):
        for team_name in NHL_TEAMS.keys():
            self.scrapeTeamRoster(team_name)

    # Get roster for specific team
    def scrapeTeamRoster(self, team_name):
        endpoint = getTeamEndpoint(team_name, "roster")
        if not endpoint:
            print(f"Team '{team_name}' not found in NHL_TEAMS.")
            return
        
        soup = self.fetchPage(endpoint)
        if soup:
            self.parseRoster(soup, team_name)
        else:
            print(f"Failed to fetch roster for {team_name}")

    # Parse HTML for team roster
    def parseRoster(self, soup, team_name):
        roster_tables = soup.find_all("div", class_="Table__Scroller")
        if not roster_tables:
            print(f"No roster tables found for {team_name}")
            return
        
        player_data = []
        for table in roster_tables:
            rows = table.find_all("tr", class_="Table__TR")
            if not rows:
                print(f"No rows found in a roster table for {team_name}")
                continue
            
            for row in rows:
                if "Table__header" in row.get("class", []):
                    continue
                cols = row.find_all("td", class_="Table__TD")
                if len(cols) >= 2:
                    name_cell = cols[1]  # Second column has name + number
                    link = name_cell.find("a")  # Look for player link
                    if link and "href" in link.attrs:
                        href = link["href"]  # e.g., "/nhl/player/_/id/12345/david-pastrnak"
                        player_id = href.split("/id/")[1].split("/")[0]  # Extract "12345"
                        name_with_number = name_cell.text.strip()
                        name = ''.join(filter(lambda x: not x.isdigit(), name_with_number)).strip()
                        if name:
                            player_data.append({"name": name, "id": player_id})
        
        if player_data:
            self.team_rosters[team_name] = player_data
            print(f"Parsed {len(player_data)} players for {team_name}")
        else:
            print(f"No players parsed for {team_name}")

    def printRoster(self):
        """Print all scraped team rosters (player names and IDs)."""
        if not self.team_rosters:
            print("No rosters to display.")
            return
        for team_name, players in self.team_rosters.items():
            print(f"\nRoster for {team_name} ({len(players)} players):")
            print("-" * 40)
            for player in players:
                print(f"{player['name']} (ID: {player['id']})")
            print("-" * 40)

    # Get team players if they have already been scraped
    def getTeamPlayers(self, team_name):
        return self.team_rosters.get(team_name, [])

if __name__ == "__main__":
    scraper = RosterScraper()
    scraper.scrapeTeamRoster("Boston Bruins")
    scraper.printRoster()