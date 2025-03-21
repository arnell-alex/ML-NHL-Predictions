# nhl_scraper_project/NHLBettingManager.py
from scrapers.draftkings.DraftKingsOddsScraper import DraftKingsOddsScraper
from databases.NHLDatabase import NHLDatabase

class NHLBettingManager:
    def __init__(self):
        """Initialize the betting manager."""
        self.scraper = DraftKingsOddsScraper()
        self.db = NHLDatabase()

    def scrape_and_store_odds(self):
        """Scrape odds from DraftKings and store them in the database."""
        print("Scraping odds from DraftKings...")
        odds = self.scraper.scrapeTonightOdds()
        if odds:
            # THE DRAFT KINGS SCRAPER DOES NOT CURRENTLY RETURN ANY DATA BY DESIGN, NEED TO UPDATE TO RETURN ODDS STRUCTURE
            print("Odds scraped successfully:")
            self.scraper.printOdds()
            print("Writing odds to database...")
            self.db.write(odds)
        else:
            print("No odds scraped to store.")
        return odds

    def close(self):
        """Close the database connection."""
        self.db.close()

if __name__ == "__main__":
    manager = NHLBettingManager()
    manager.scrape_and_store_odds()
    manager.close()