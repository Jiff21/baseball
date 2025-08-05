"""
Hitting Statistics Service for fetching and processing MLB hitting data.
This service fetches data from three APIs: lefty splits, righty splits, and overall stats.
"""
import requests
import logging
from typing import Dict, List, Optional
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class HittingStatsService:
    """Service for fetching hitting statistics from MLB APIs."""
    
    def __init__(self, season=None):
        self.season = season or datetime.now().year
        self.base_url = "https://bdfed.stitch.mlbinfra.com/bdfed/stats/team"
        self.standings_url = "https://bdfed.stitch.mlbinfra.com/bdfed/transform-mlb-standings"
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
    
    def fetch_all_hitting_stats(self) -> Dict[str, Dict]:
        """
        Fetch hitting statistics for all three split types.
        
        Returns:
            Dict with keys 'lefty', 'righty', 'overall' containing team stats
        """
        logger.info(f"Starting hitting statistics fetch for {self.season} season...")
        
        try:
            # Fetch wins/losses splits from standings API
            wins_losses_data = self._fetch_wins_losses_splits()
            
            # Fetch hitting stats from all three APIs
            lefty_stats = self._fetch_hitting_stats('lefty')
            righty_stats = self._fetch_hitting_stats('righty')
            overall_stats = self._fetch_hitting_stats('overall')
            
            # Combine stats with wins/losses
            combined_stats = {
                'lefty': self._combine_stats_with_wins_losses(lefty_stats, wins_losses_data, 'lefty'),
                'righty': self._combine_stats_with_wins_losses(righty_stats, wins_losses_data, 'righty'),
                'overall': self._combine_stats_with_wins_losses(overall_stats, wins_losses_data, 'overall')
            }
            
            logger.info(f"Successfully fetched hitting stats for all splits")
            return combined_stats
            
        except Exception as e:
            logger.error(f"Error fetching hitting stats: {e}")
            raise
    
    def _fetch_hitting_stats(self, split_type: str) -> Dict:
        """
        Fetch hitting statistics for a specific split type.
        
        Args:
            split_type: 'lefty', 'righty', or 'overall'
            
        Returns:
            Dictionary of team hitting statistics
        """
        params = {
            'env': 'prod',
            'gameType': 'R',
            'group': 'hitting',
            'order': 'desc',
            'sortStat': 'homeRuns',
            'stats': 'season',
            'season': str(self.season),
            'limit': '30',
            'offset': '0'
        }
        
        # Add split-specific parameters
        if split_type == 'lefty':
            params['sitCodes'] = 'vl'  # vs lefty pitchers
        elif split_type == 'righty':
            params['sitCodes'] = 'vr'  # vs righty pitchers
        # overall has no sitCodes parameter
        
        logger.info(f"Fetching {split_type} hitting stats...")
        
        response = self.session.get(self.base_url, params=params)
        response.raise_for_status()
        data = response.json()
        
        # Convert to dict keyed by team abbreviation
        team_stats = {}
        for team in data.get('stats', []):
            team_abbrev = team.get('teamAbbrev')
            if team_abbrev:
                team_stats[team_abbrev] = self._process_hitting_data(team)
        
        logger.info(f"Fetched {split_type} hitting stats for {len(team_stats)} teams")
        return team_stats
    
    def _process_hitting_data(self, raw_data: Dict) -> Dict:
        """
        Process raw hitting data from API into standardized format.
        
        Args:
            raw_data: Raw team data from API
            
        Returns:
            Processed team hitting statistics
        """
        # Calculate singles from hits minus extra base hits
        hits = int(raw_data.get('hits', 0))
        doubles = int(raw_data.get('doubles', 0))
        triples = int(raw_data.get('triples', 0))
        home_runs = int(raw_data.get('homeRuns', 0))
        singles = hits - doubles - triples - home_runs
        
        # Ensure singles is not negative (data quality check)
        singles = max(0, singles)
        
        return {
            'team_abbreviation': raw_data.get('teamAbbrev', ''),
            'team_name': raw_data.get('teamName', ''),
            'games': int(raw_data.get('gamesPlayed', 0)),
            'plate_appearances': int(raw_data.get('plateAppearances', 0)),
            'at_bats': int(raw_data.get('atBats', 0)),
            'runs': int(raw_data.get('runs', 0)),
            'hits': hits,
            'singles': singles,
            'doubles': doubles,
            'triples': triples,
            'home_runs': home_runs,
            'rbis': int(raw_data.get('rbi', 0)),
            'walks': int(raw_data.get('baseOnBalls', 0)),
            'intentional_walks': int(raw_data.get('intentionalWalks', 0)),
            'hit_by_pitch': int(raw_data.get('hitByPitch', 0)),
            'strikeouts': int(raw_data.get('strikeOuts', 0)),
            'stolen_bases': int(raw_data.get('stolenBases', 0)),
            'caught_stealing': int(raw_data.get('caughtStealing', 0)),
            'total_bases': int(raw_data.get('totalBases', 0)),
        }
    
    def _fetch_wins_losses_splits(self) -> Dict:
        """
        Fetch wins/losses splits from standings API.
        
        Returns:
            Dictionary with team wins/losses by split type
        """
        current_date = datetime.now().strftime('%Y-%m-%d')
        
        params = {
            'splitPcts': 'false',
            'numberPcts': 'false',
            'standingsView': 'division',
            'sortTemplate': '3',
            'season': str(self.season),
            'leagueIds': ['103', '104'],  # AL and NL
            'standingsTypes': 'regularSeason',
            'contextTeamId': '',
            'teamId': '',
            'date': current_date,
            'hydrateAlias': 'noSchedule',
            'sortDivisions': '201,202,200,204,205,203',
            'sortLeagues': '103,104,115,114',
            'sortSports': '1'
        }
        
        logger.info("Fetching wins/losses splits from standings API...")
        
        response = self.session.get(self.standings_url, params=params)
        response.raise_for_status()
        data = response.json()
        
        wins_losses_data = {}
        
        if 'records' in data:
            for record in data['records']:
                if 'teamRecords' in record:
                    for team_record in record['teamRecords']:
                        team_info = team_record.get('team', {})
                        team_abbrev = team_info.get('abbreviation')
                        
                        if team_abbrev:
                            # Parse record_right and record_left
                            record_right = team_record.get('record_right', '0-0')
                            record_left = team_record.get('record_left', '0-0')
                            overall_wins = team_record.get('wins', 0)
                            overall_losses = team_record.get('losses', 0)
                            
                            try:
                                right_wins, right_losses = map(int, record_right.split('-'))
                                left_wins, left_losses = map(int, record_left.split('-'))
                                
                                wins_losses_data[team_abbrev] = {
                                    'lefty': {'wins': left_wins, 'losses': left_losses},
                                    'righty': {'wins': right_wins, 'losses': right_losses},
                                    'overall': {'wins': overall_wins, 'losses': overall_losses}
                                }
                            except (ValueError, AttributeError) as e:
                                logger.warning(f"Could not parse wins/losses for {team_abbrev}: {e}")
                                wins_losses_data[team_abbrev] = {
                                    'lefty': {'wins': 0, 'losses': 0},
                                    'righty': {'wins': 0, 'losses': 0},
                                    'overall': {'wins': overall_wins, 'losses': overall_losses}
                                }
        
        logger.info(f"Fetched wins/losses splits for {len(wins_losses_data)} teams")
        return wins_losses_data
    
    def _combine_stats_with_wins_losses(self, hitting_stats: Dict, wins_losses_data: Dict, split_type: str) -> Dict:
        """
        Combine hitting statistics with wins/losses data.
        
        Args:
            hitting_stats: Hitting statistics by team
            wins_losses_data: Wins/losses data by team and split
            split_type: 'lefty', 'righty', or 'overall'
            
        Returns:
            Combined statistics dictionary
        """
        combined_stats = {}
        
        for team_abbrev, stats in hitting_stats.items():
            # Get wins/losses for this team and split
            team_wins_losses = wins_losses_data.get(team_abbrev, {})
            split_wins_losses = team_wins_losses.get(split_type, {'wins': 0, 'losses': 0})
            
            # Combine hitting stats with wins/losses
            combined_stats[team_abbrev] = {
                **stats,
                'wins': split_wins_losses['wins'],
                'losses': split_wins_losses['losses'],
                'split_type': split_type,
                'season': self.season
            }
        
        return combined_stats
    
    def get_sample_data(self) -> Dict[str, Dict]:
        """
        Generate sample hitting data for development/testing.
        
        Returns:
            Sample data in the same format as real API data
        """
        import random
        random.seed(42)  # For consistent sample data
        
        team_names = {
            'BOS': 'Boston Red Sox',
            'NYY': 'New York Yankees',
            'LAD': 'Los Angeles Dodgers',
            'HOU': 'Houston Astros',
            'ATL': 'Atlanta Braves',
        }
        
        sample_data = {'lefty': {}, 'righty': {}, 'overall': {}}
        
        for abbrev, name in team_names.items():
            for split_type in ['lefty', 'righty', 'overall']:
                # Generate realistic hitting stats
                games = random.randint(140, 162)
                pa_per_game = random.uniform(35, 42)  # Realistic PA per game
                plate_appearances = int(games * pa_per_game)
                at_bats = int(plate_appearances * random.uniform(0.85, 0.92))
                
                hits = int(at_bats * random.uniform(0.240, 0.280))  # Team batting average
                home_runs = int(hits * random.uniform(0.12, 0.18))  # HR rate
                doubles = int(hits * random.uniform(0.18, 0.25))  # 2B rate
                triples = int(hits * random.uniform(0.01, 0.03))  # 3B rate
                singles = hits - doubles - triples - home_runs
                
                walks = int(plate_appearances * random.uniform(0.08, 0.12))
                strikeouts = int(plate_appearances * random.uniform(0.20, 0.25))
                
                # Generate wins/losses
                if split_type == 'overall':
                    wins = random.randint(60, 100)
                    losses = 162 - wins
                elif split_type == 'lefty':
                    wins = random.randint(15, 35)
                    losses = random.randint(15, 35)
                else:  # righty
                    wins = random.randint(45, 75)
                    losses = random.randint(45, 75)
                
                sample_data[split_type][abbrev] = {
                    'team_abbreviation': abbrev,
                    'team_name': name,
                    'games': games,
                    'plate_appearances': plate_appearances,
                    'at_bats': at_bats,
                    'runs': int(plate_appearances * random.uniform(0.12, 0.16)),
                    'hits': hits,
                    'singles': max(0, singles),
                    'doubles': doubles,
                    'triples': triples,
                    'home_runs': home_runs,
                    'rbis': int(plate_appearances * random.uniform(0.12, 0.16)),
                    'walks': walks,
                    'intentional_walks': int(walks * random.uniform(0.05, 0.15)),
                    'hit_by_pitch': int(plate_appearances * random.uniform(0.008, 0.015)),
                    'strikeouts': strikeouts,
                    'stolen_bases': int(plate_appearances * random.uniform(0.02, 0.05)),
                    'caught_stealing': int(plate_appearances * random.uniform(0.005, 0.015)),
                    'total_bases': singles + (doubles * 2) + (triples * 3) + (home_runs * 4),
                    'wins': wins,
                    'losses': losses,
                    'split_type': split_type,
                    'season': self.season
                }
        
        return sample_data
