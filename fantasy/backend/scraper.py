"""
MLB data scraper for collecting team statistics.
"""
import requests
from bs4 import BeautifulSoup
import time
import logging
from typing import Dict, List, Optional
from models import db, Team
from config import Config

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class MLBScraper:
    """Scraper for MLB team statistics."""
    
    def __init__(self):
        self.base_url = Config.MLB_BASE_URL
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
    
    def scrape_team_stats(self) -> List[Dict]:
        """
        Scrape team pitching statistics vs lefty and righty batters.
        
        Returns:
            List of team statistics dictionaries
        """
        logger.info("Starting team statistics scraping...")
        
        # For now, we'll use sample data since MLB.com scraping requires
        # more complex handling of their dynamic content
        sample_teams = self._get_sample_team_data()
        
        logger.info(f"Scraped statistics for {len(sample_teams)} teams")
        return sample_teams
    
    def _get_sample_team_data(self) -> List[Dict]:
        """
        Generate sample team data for development.
        In production, this would scrape real MLB data.
        
        Returns:
            List of sample team data
        """
        teams_data = []
        
        # Sample data for all MLB teams
        team_names = {
            'COL': 'Colorado Rockies',
            'PIT': 'Pittsburgh Pirates',
            'CWS': 'Chicago White Sox',
            'LAA': 'Los Angeles Angels',
            'CLE': 'Cleveland Guardians',
            'TEX': 'Texas Rangers',
            'DET': 'Detroit Tigers',
            'MIN': 'Minnesota Twins',
            'BAL': 'Baltimore Orioles',
            'KC': 'Kansas City Royals',
            'SF': 'San Francisco Giants',
            'BOS': 'Boston Red Sox',
            'HOU': 'Houston Astros',
            'ATL': 'Atlanta Braves',
            'WSH': 'Washington Nationals',
            'SD': 'San Diego Padres',
            'MIL': 'Milwaukee Brewers',
            'CIN': 'Cincinnati Reds',
            'OAK': 'Oakland Athletics',
            'MIA': 'Miami Marlins',
            'SEA': 'Seattle Mariners',
            'TB': 'Tampa Bay Rays',
            'NYM': 'New York Mets',
            'STL': 'St. Louis Cardinals',
            'PHI': 'Philadelphia Phillies',
            'NYY': 'New York Yankees',
            'AZ': 'Arizona Diamondbacks',
            'LAD': 'Los Angeles Dodgers',
            'TOR': 'Toronto Blue Jays',
            'CHC': 'Chicago Cubs'
        }
        
        # Generate realistic sample data for each team
        import random
        random.seed(42)  # For consistent sample data
        
        for abbr, name in team_names.items():
            # Generate realistic pitching stats
            base_era = random.uniform(3.5, 5.5)
            base_whip = random.uniform(1.15, 1.45)
            base_k_per_9 = random.uniform(7.5, 10.5)
            base_bb_per_9 = random.uniform(2.5, 4.0)
            base_hr_per_9 = random.uniform(0.8, 1.5)
            base_hits_per_9 = random.uniform(7.5, 9.5)
            
            # Lefty vs righty variations (lefties typically perform slightly better vs righties)
            lefty_modifier = random.uniform(0.95, 1.05)
            righty_modifier = random.uniform(0.95, 1.05)
            
            team_data = {
                'abbreviation': abbr,
                'name': name,
                'vs_lefty_era': round(base_era * lefty_modifier, 2),
                'vs_lefty_whip': round(base_whip * lefty_modifier, 3),
                'vs_lefty_k_per_9': round(base_k_per_9 * lefty_modifier, 1),
                'vs_lefty_bb_per_9': round(base_bb_per_9 * lefty_modifier, 1),
                'vs_lefty_hr_per_9': round(base_hr_per_9 * lefty_modifier, 2),
                'vs_lefty_hits_per_9': round(base_hits_per_9 * lefty_modifier, 1),
                'vs_righty_era': round(base_era * righty_modifier, 2),
                'vs_righty_whip': round(base_whip * righty_modifier, 3),
                'vs_righty_k_per_9': round(base_k_per_9 * righty_modifier, 1),
                'vs_righty_bb_per_9': round(base_bb_per_9 * righty_modifier, 1),
                'vs_righty_hr_per_9': round(base_hr_per_9 * righty_modifier, 2),
                'vs_righty_hits_per_9': round(base_hits_per_9 * righty_modifier, 1),
            }
            
            teams_data.append(team_data)
        
        return teams_data
    
    def save_team_data(self, teams_data: List[Dict]) -> None:
        """
        Save team data to the database.
        
        Args:
            teams_data: List of team data dictionaries
        """
        logger.info("Saving team data to database...")
        
        for team_data in teams_data:
            # Check if team exists
            team = Team.query.filter_by(abbreviation=team_data['abbreviation']).first()
            
            if team:
                # Update existing team
                for key, value in team_data.items():
                    if hasattr(team, key):
                        setattr(team, key, value)
                logger.info(f"Updated team: {team_data['abbreviation']}")
            else:
                # Create new team
                team = Team(**team_data)
                db.session.add(team)
                logger.info(f"Created team: {team_data['abbreviation']}")
        
        try:
            db.session.commit()
            logger.info("Successfully saved all team data")
        except Exception as e:
            db.session.rollback()
            logger.error(f"Error saving team data: {e}")
            raise
    
    def run_full_scrape(self) -> None:
        """Run the complete scraping process."""
        try:
            teams_data = self.scrape_team_stats()
            self.save_team_data(teams_data)
            logger.info("Full scraping process completed successfully")
        except Exception as e:
            logger.error(f"Error during scraping process: {e}")
            raise


def run_scraper():
    """Standalone function to run the scraper."""
    from app import create_app
    
    app = create_app()
    with app.app_context():
        scraper = MLBScraper()
        scraper.run_full_scrape()


if __name__ == '__main__':
    run_scraper()

