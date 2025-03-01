from scrapers.espn.NHLScraper import NHLScraper

class PlayerStatsScraper(NHLScraper):
    def __init__(self):
        super().__init__()
        # Key: player name, Value: dict of stats
        self.player_stats = {}  

    # Get player stats by ESPN ID
    def scrapePlayerStats(self, player_name, player_id):
        endpoint = f"player/stats/_/id/{player_id}"
        soup = self.fetchPage(endpoint)
        if soup:
            self.parseStats(soup, player_name)
        else:
            print(f"Failed to fetch stats for {player_name}")

    def scrapeTeamPlayers(self, team_players):
        """Scrape stats for all players in a team roster."""
        for player in team_players:
            self.scrapePlayerStats(player["name"], player["id"])

    def parseStats(self, soup, player_name):
        # Get position
        header = soup.select_one('div[class^="PlayerHeader__Team"]')
        position = "N/A"  # Default if not found
        if header:
            list_items = header.find_all("li")
            if len(list_items) >= 2:  # Second <li> should be position
                position = list_items[1].text.strip()

        # Get stats 
        stats_section = soup.find("div", class_="Table__Scroller")
        if not stats_section:
            print(f"No stats section (Table__Scroller) found for {player_name}")
            return
        stats_table = stats_section.find("tbody", class_="Table__TBODY")
        if not stats_table:
            print(f"No stats table body found for {player_name}")
            return
        season_rows = stats_table.find_all("tr", class_="Table__TR")
        if not season_rows:
            print(f"No stats season__rows found for {player_name}")
            return
        
        # Get the most recent season row (first row)
        latest_season_row = season_rows[0]
        cols = latest_season_row.find_all("td", class_="Table__TD")
        if not cols:
            print(f"No columns found for {player_name}")
            return

        # Define stats based on skaters vs goaltenders
        if position == "Goaltender":
            stats = {
                "position": position,
                "games_played": cols[0].text.strip() if len(cols) > 0 else "0",
                "games_started": cols[1].text.strip() if len(cols) > 1 else "0",
                "wins": cols[2].text.strip() if len(cols) > 2 else "0",
                "losses": cols[3].text.strip() if len(cols) > 3 else "0",
                "ot_losses": cols[4].text.strip() if len(cols) > 4 else "0",
                "goals_against": cols[5].text.strip() if len(cols) > 5 else "0",
                "shots_against": cols[6].text.strip() if len(cols) > 6 else "0",
                "saves": cols[7].text.strip() if len(cols) > 7 else "0",
                "save_percentage": cols[8].text.strip() if len(cols) > 8 else ".000",
                "goals_against_avg": cols[9].text.strip() if len(cols) > 9 else "0.00",
                "shutouts": cols[10].text.strip() if len(cols) > 10 else "0",
                "time_on_ice": cols[11].text.strip() if len(cols) > 11 else "0"
            }
        else:
            stats = {
                "position": position,
                "games_played": cols[0].text.strip() if len(cols) > 0 else "0",
                "goals": cols[1].text.strip() if len(cols) > 1 else "0",
                "assists": cols[2].text.strip() if len(cols) > 2 else "0",
                "points": cols[3].text.strip() if len(cols) > 3 else "0",
                "plus_minus": cols[4].text.strip() if len(cols) > 4 else "0",
                "pim": cols[5].text.strip() if len(cols) > 5 else "0",
                "shots": cols[6].text.strip() if len(cols) > 6 else "0",
                "power_play_goals": cols[7].text.strip() if len(cols) > 7 else "0",
                "power_play_points": cols[8].text.strip() if len(cols) > 8 else "0",
                "shorthanded_goals": cols[9].text.strip() if len(cols) > 9 else "0",
                "shorthanded_points": cols[10].text.strip() if len(cols) > 10 else "0",
                "game_winning_goals": cols[11].text.strip() if len(cols) > 11 else "0",
                "overtime_goals": cols[12].text.strip() if len(cols) > 12 else "0",
                "shots_pct": cols[13].text.strip() if len(cols) > 13 else ".0",
                "faceoff_pct": cols[14].text.strip() if len(cols) > 14 else ".0",
                "time_on_ice_avg": cols[15].text.strip() if len(cols) > 15 else "0:00"
            }
        
        self.player_stats[player_name] = stats
        print(f"Parsed stats for {player_name} (Position: {position})")

    def printStats(self):
        if not self.player_stats:
            print("No player stats to display.")
            return
        
        print("\nPlayer Stats:")
        # Separate headers for skaters and goaltenders
        skater_header = f"{'Name':<20} {'P':>3} {'GP':>5} {'G':>5} {'A':>5} {'PTS':>5} {'+/-':>5} {'PIM':>5} {'S':>5} {'PPG':>5} {'PPP':>5} {'SHG':>5} {'SHP':>5} {'GWG':>5} {'OTG':>5} {'S%':>5} {'FO%':>5} {'TOI':>6}"
        goalie_header = f"{'Name':<20} {'P':>3} {'GP':>5} {'GS':>5} {'W':>5} {'L':>5} {'OTL':>5} {'GA':>5} {'SA':>5} {'SV':>5} {'SV%':>6} {'GAA':>6} {'SO':>5} {'TOI':>6}"
        
        skaters = {k: v for k, v in self.player_stats.items() if v["position"] != "Goaltender"}
        goalies = {k: v for k, v in self.player_stats.items() if v["position"] == "Goaltender"}

        if skaters:
            print("\nSkaters:")
            print("-" * 110)
            print(skater_header)
            print("-" * 110)
            for name, stats in skaters.items():
                print(f"{name:<20} {stats['position']:>3} {stats['games_played']:>5} {stats['goals']:>5} {stats['assists']:>5} {stats['points']:>5} {stats['plus_minus']:>5} {stats['pim']:>5} {stats['shots']:>5} {stats['power_play_goals']:>5} {stats['power_play_points']:>5} {stats['shorthanded_goals']:>5} {stats['shorthanded_points']:>5} {stats['game_winning_goals']:>5} {stats['overtime_goals']:>5} {stats['shots_pct']:>5} {stats['faceoff_pct']:>5} {stats['time_on_ice_avg']:>6}")
            print("-" * 110)

        if goalies:
            print("\nGoaltenders:")
            print("-" * 95)
            print(goalie_header)
            print("-" * 95)
            for name, stats in goalies.items():
                print(f"{name:<20} {stats['position']:>3} {stats['games_played']:>5} {stats['games_started']:>5} {stats['wins']:>5} {stats['losses']:>5} {stats['ot_losses']:>5} {stats['goals_against']:>5} {stats['shots_against']:>5} {stats['saves']:>5} {stats['save_percentage']:>6} {stats['goals_against_avg']:>6} {stats['shutouts']:>5} {stats['time_on_ice']:>6}")
            print("-" * 95)

    def getPlayerStats(self, player_name):
        return self.player_stats.get(player_name, {})

if __name__ == "__main__":
    from scrapers.espn.RosterScraper import RosterScraper
    roster_scraper = RosterScraper()
    roster_scraper.scrapeTeamRoster("Boston Bruins")
    players = roster_scraper.getTeamPlayers("Boston Bruins")
    stats_scraper = PlayerStatsScraper()
    stats_scraper.scrapeTeamPlayers(players)
    stats_scraper.printStats()