# nhl_scraper_project/databases/NHLDatabase.py
import sqlite3
from datetime import datetime

class NHLDatabase:
    def __init__(self, db_path="databases/NHLDatabase.db"):
        """Initialize SQLite connection and create tables."""
        self.conn = sqlite3.connect(db_path)
        self.createTables()

    def createTables(self):
        """Create SQLite tables for games, team odds, and total points."""
        cursor = self.conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Games (
                game_id INTEGER PRIMARY KEY AUTOINCREMENT,
                date DATE,
                team1_name TEXT,
                team2_name TEXT,
                UNIQUE(date, team1_name, team2_name)
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS TeamOdds (
                odds_id INTEGER PRIMARY KEY AUTOINCREMENT,
                game_id INTEGER,
                team_name TEXT,
                spread_points REAL,
                spread_odds INTEGER,
                moneyline INTEGER,
                FOREIGN KEY (game_id) REFERENCES Games(game_id)
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS TotalPoints (
                total_id INTEGER PRIMARY KEY AUTOINCREMENT,
                game_id INTEGER,
                over_points REAL,
                over_odds INTEGER,
                under_points REAL,
                under_odds INTEGER,
                FOREIGN KEY (game_id) REFERENCES Games(game_id)
            )
        """)
        self.conn.commit()

    def writeGameOdds(self, game_odds):
        """Write game odds dictionary to the database."""
        cursor = self.conn.cursor()
        for matchup, data in game_odds.items():
            cursor.execute("""
                INSERT OR IGNORE INTO Games (date, team1_name, team2_name)
                VALUES (?, ?, ?)
            """, (data["date"], list(data["teams"].keys())[0], list(data["teams"].keys())[1]))
            cursor.execute("SELECT game_id FROM Games WHERE date = ? AND team1_name = ? AND team2_name = ?",
                           (data["date"], list(data["teams"].keys())[0], list(data["teams"].keys())[1]))
            game_id = cursor.fetchone()[0]

            for team_name, team_data in data["teams"].items():
                cursor.execute("""
                    INSERT INTO TeamOdds (game_id, team_name, spread_points, spread_odds, moneyline)
                    VALUES (?, ?, ?, ?, ?)
                """, (game_id, team_name, team_data["spread"]["points"], team_data["spread"]["odds"], team_data["moneyline"]))

            total = data["total_points"]
            cursor.execute("""
                INSERT INTO TotalPoints (game_id, over_points, over_odds, under_points, under_odds)
                VALUES (?, ?, ?, ?, ?)
            """, (game_id, total["over"]["points"], total["over"]["odds"], total["under"]["points"], total["under"]["odds"]))

        self.conn.commit()
        print(f"Saved {len(game_odds)} games to database")

    def read(self, date=None):
        """Read odds from the database for a specific date."""
        cursor = self.conn.cursor()
        if date:
            cursor.execute("""
                SELECT g.game_id, g.date, g.team1_name, g.team2_name, 
                       t1.spread_points, t1.spread_odds, t1.moneyline,
                       t2.spread_points, t2.spread_odds, t2.moneyline,
                       tp.over_points, tp.over_odds, tp.under_points, tp.under_odds
                FROM Games g
                LEFT JOIN TeamOdds t1 ON g.game_id = t1.game_id AND t1.team_name = g.team1_name
                LEFT JOIN TeamOdds t2 ON g.game_id = t2.game_id AND t2.team_name = g.team2_name
                LEFT JOIN TotalPoints tp ON g.game_id = tp.game_id
                WHERE g.date = ?
            """, (date,))
        else:
            cursor.execute("""
                SELECT g.game_id, g.date, g.team1_name, g.team2_name, 
                       t1.spread_points, t1.spread_odds, t1.moneyline,
                       t2.spread_points, t2.spread_odds, t2.moneyline,
                       tp.over_points, tp.over_odds, tp.under_points, tp.under_ods
                FROM Games g
                LEFT JOIN TeamOdds t1 ON g.game_id = t1.game_id AND t1.team_name = g.team1_name
                LEFT JOIN TeamOdds t2 ON g.game_id = t2.game_id AND t2.team_name = g.team2_name
                LEFT JOIN TotalPoints tp ON g.game_id = tp.game_id
            """)
        rows = cursor.fetchall()
        odds_dict = {}
        for row in rows:
            game_id, date, team1, team2, t1_sp, t1_so, t1_ml, t2_sp, t2_so, t2_ml, over_p, over_o, under_p, under_o = row
            matchup = f"{team1} vs. {team2}"
            odds_dict[matchup] = {
                "date": date,
                "teams": {
                    team1: {"spread": {"points": t1_sp, "odds": t1_so}, "moneyline": t1_ml},
                    team2: {"spread": {"points": t2_sp, "odds": t2_so}, "moneyline": t2_ml}
                },
                "total_points": {
                    "over": {"points": over_p, "odds": over_o},
                    "under": {"points": under_p, "odds": under_o}
                }
            }
        return odds_dict

    def close(self):
        """Close the database connection."""
        self.conn.close()

if __name__ == "__main__":
    db = NHLDatabase()
    sample_odds = {
        "Boston Bruins vs. Toronto": {
            "teams": {
                "Boston Bruins": {"spread": {"points": -1.5, "odds": -110}, "moneyline": -150},
                "Toronto": {"spread": {"points": 1.5, "odds": -110}, "moneyline": 130}
            },
            "total_points": {"over": {"points": 5.5, "odds": -105}, "under": {"points": 5.5, "odds": -115}},
            "date": "2025-03-16"
        }
    }
    db.writeGameOdds(sample_odds)
    odds = db.read("2025-03-16")
    print(odds)
    db.close()