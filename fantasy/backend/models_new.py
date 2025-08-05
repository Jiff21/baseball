"""
New database models for the Fantasy Baseball application - Hitting Stats Focus.
This replaces the old pitching-focused models with a hitting-based approach.
"""
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import JSON, Index

db = SQLAlchemy()

class ScoringSettings:
    """Default scoring settings for different league types."""
    
    class Batting:
        S = 1      # Singles
        D = 2      # Doubles
        T = 3      # Triples
        HR = 4     # Home Runs
        BB = 1     # Walks
        IBB = 1    # Intentional Walks
        HBP = 1    # Hit By Pitch
        R = 1      # Runs
        RBI = 1    # Runs Batted In
        SB = 2     # Stolen Base
        CS = -1    # Caught Stealing
        SO = -1    # Strike Outs
        TB = 0.25  # Total Bases (per base)

    class Pitching:
        BB = -1.0    # Walks Issued
        IBB = -1.0   # IBB
        ER = -1.0    # Earned Runs
        HA = -1.0    # Hits allowed
        HB = -1.0    # Hit Batters
        HRA = -3.0   # HRA
        INN = 3.0    # Innings (3 outs)
        K = 1.0      # Strikeouts
        W = 5.0      # Wins
        L = -3.0     # Losses
        S = 5.0      # Saves
        BS = 0.0     # Blown Saves
        QS = 0.0     # Quality Starts
        TB = -0.25   # Total Bases Allowed (per base)

    @classmethod
    def get_default_settings(cls):
        """Get default scoring settings."""
        return {
            'batting': {
                'S': cls.Batting.S,
                'D': cls.Batting.D,
                'T': cls.Batting.T,
                'HR': cls.Batting.HR,
                'BB': cls.Batting.BB,
                'IBB': cls.Batting.IBB,
                'HBP': cls.Batting.HBP,
                'R': cls.Batting.R,
                'RBI': cls.Batting.RBI,
                'SB': cls.Batting.SB,
                'CS': cls.Batting.CS,
                'SO': cls.Batting.SO,
                'TB': cls.Batting.TB,
            },
            'pitching': {
                'BB': cls.Pitching.BB,
                'IBB': cls.Pitching.IBB,
                'ER': cls.Pitching.ER,
                'HA': cls.Pitching.HA,
                'HB': cls.Pitching.HB,
                'HRA': cls.Pitching.HRA,
                'INN': cls.Pitching.INN,
                'K': cls.Pitching.K,
                'W': cls.Pitching.W,
                'L': cls.Pitching.L,
                'S': cls.Pitching.S,
                'BS': cls.Pitching.BS,
                'QS': cls.Pitching.QS,
                'TB': cls.Pitching.TB,
            }
        }


class TeamHittingStats(db.Model):
    """Model for storing raw hitting statistics by team and split type."""
    
    __tablename__ = 'team_hitting_stats'
    
    id = db.Column(db.Integer, primary_key=True)
    team_abbreviation = db.Column(db.String(3), nullable=False)
    team_name = db.Column(db.String(100), nullable=False)
    split_type = db.Column(db.String(10), nullable=False)  # 'lefty', 'righty', 'overall'
    season = db.Column(db.Integer, nullable=False)
    
    # Raw hitting statistics
    games = db.Column(db.Integer, default=0)
    plate_appearances = db.Column(db.Integer, default=0)
    at_bats = db.Column(db.Integer, default=0)
    runs = db.Column(db.Integer, default=0)
    hits = db.Column(db.Integer, default=0)
    singles = db.Column(db.Integer, default=0)
    doubles = db.Column(db.Integer, default=0)
    triples = db.Column(db.Integer, default=0)
    home_runs = db.Column(db.Integer, default=0)
    rbis = db.Column(db.Integer, default=0)
    walks = db.Column(db.Integer, default=0)
    intentional_walks = db.Column(db.Integer, default=0)
    hit_by_pitch = db.Column(db.Integer, default=0)
    strikeouts = db.Column(db.Integer, default=0)
    stolen_bases = db.Column(db.Integer, default=0)
    caught_stealing = db.Column(db.Integer, default=0)
    total_bases = db.Column(db.Integer, default=0)
    
    # Wins/Losses (from standings API)
    wins = db.Column(db.Integer, default=0)
    losses = db.Column(db.Integer, default=0)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Indexes for performance
    __table_args__ = (
        Index('idx_team_split_season', 'team_abbreviation', 'split_type', 'season'),
        Index('idx_team_season', 'team_abbreviation', 'season'),
    )
    
    def __repr__(self):
        return f'<TeamHittingStats {self.team_abbreviation} {self.split_type} {self.season}>'
    
    def to_dict(self):
        """Convert to dictionary for API responses."""
        return {
            'id': self.id,
            'team_abbreviation': self.team_abbreviation,
            'team_name': self.team_name,
            'split_type': self.split_type,
            'season': self.season,
            'games': self.games,
            'plate_appearances': self.plate_appearances,
            'at_bats': self.at_bats,
            'runs': self.runs,
            'hits': self.hits,
            'singles': self.singles,
            'doubles': self.doubles,
            'triples': self.triples,
            'home_runs': self.home_runs,
            'rbis': self.rbis,
            'walks': self.walks,
            'intentional_walks': self.intentional_walks,
            'hit_by_pitch': self.hit_by_pitch,
            'strikeouts': self.strikeouts,
            'stolen_bases': self.stolen_bases,
            'caught_stealing': self.caught_stealing,
            'total_bases': self.total_bases,
            'wins': self.wins,
            'losses': self.losses,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
        }


class TeamCalculatedStats(db.Model):
    """Model for storing calculated per-plate-appearance rates."""
    
    __tablename__ = 'team_calculated_stats'
    
    id = db.Column(db.Integer, primary_key=True)
    team_abbreviation = db.Column(db.String(3), nullable=False)
    split_type = db.Column(db.String(10), nullable=False)  # 'lefty', 'righty', 'overall'
    season = db.Column(db.Integer, nullable=False)
    
    # Per-plate-appearance rates
    strikeouts_per_pa = db.Column(db.Float, default=0.0)
    runs_per_pa = db.Column(db.Float, default=0.0)
    walks_per_pa = db.Column(db.Float, default=0.0)
    singles_per_pa = db.Column(db.Float, default=0.0)
    doubles_per_pa = db.Column(db.Float, default=0.0)
    triples_per_pa = db.Column(db.Float, default=0.0)
    home_runs_per_pa = db.Column(db.Float, default=0.0)
    total_bases_per_pa = db.Column(db.Float, default=0.0)
    ibb_per_pa = db.Column(db.Float, default=0.0)
    hbp_per_pa = db.Column(db.Float, default=0.0)
    rbis_per_pa = db.Column(db.Float, default=0.0)
    stolen_bases_per_pa = db.Column(db.Float, default=0.0)
    caught_stealing_per_pa = db.Column(db.Float, default=0.0)
    
    # Plate appearances per inning: (PA/Games)/9
    pa_per_inning = db.Column(db.Float, default=0.0)
    
    # Wins/losses per game
    wins_per_game = db.Column(db.Float, default=0.0)
    losses_per_game = db.Column(db.Float, default=0.0)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Indexes for performance
    __table_args__ = (
        Index('idx_calc_team_split_season', 'team_abbreviation', 'split_type', 'season'),
    )
    
    def __repr__(self):
        return f'<TeamCalculatedStats {self.team_abbreviation} {self.split_type} {self.season}>'
    
    def to_dict(self):
        """Convert to dictionary for API responses."""
        return {
            'id': self.id,
            'team_abbreviation': self.team_abbreviation,
            'split_type': self.split_type,
            'season': self.season,
            'strikeouts_per_pa': self.strikeouts_per_pa,
            'runs_per_pa': self.runs_per_pa,
            'walks_per_pa': self.walks_per_pa,
            'singles_per_pa': self.singles_per_pa,
            'doubles_per_pa': self.doubles_per_pa,
            'triples_per_pa': self.triples_per_pa,
            'home_runs_per_pa': self.home_runs_per_pa,
            'total_bases_per_pa': self.total_bases_per_pa,
            'ibb_per_pa': self.ibb_per_pa,
            'hbp_per_pa': self.hbp_per_pa,
            'rbis_per_pa': self.rbis_per_pa,
            'stolen_bases_per_pa': self.stolen_bases_per_pa,
            'caught_stealing_per_pa': self.caught_stealing_per_pa,
            'pa_per_inning': self.pa_per_inning,
            'wins_per_game': self.wins_per_game,
            'losses_per_game': self.losses_per_game,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
        }


class ExpectedGame(db.Model):
    """Model for storing expected game calculations based on starter innings."""
    
    __tablename__ = 'expected_games'
    
    id = db.Column(db.Integer, primary_key=True)
    team_abbreviation = db.Column(db.String(3), nullable=False)
    handedness = db.Column(db.String(10), nullable=False)  # 'lefty' or 'righty'
    starter_expected_innings = db.Column(db.Float, default=6.0)
    league_type = db.Column(db.String(20), nullable=False)  # 'Custom', 'ESPN', 'CBS', 'Yahoo'
    scoring_settings = db.Column(JSON)  # JSON field for scoring settings
    season = db.Column(db.Integer, nullable=False)
    
    # Expected plate appearances and stats
    expected_plate_appearances = db.Column(db.Float, default=0.0)
    expected_fantasy_points = db.Column(db.Float, default=0.0)
    expected_runs = db.Column(db.Float, default=0.0)
    expected_hits = db.Column(db.Float, default=0.0)
    expected_singles = db.Column(db.Float, default=0.0)
    expected_doubles = db.Column(db.Float, default=0.0)
    expected_triples = db.Column(db.Float, default=0.0)
    expected_home_runs = db.Column(db.Float, default=0.0)
    expected_walks = db.Column(db.Float, default=0.0)
    expected_strikeouts = db.Column(db.Float, default=0.0)
    expected_total_bases = db.Column(db.Float, default=0.0)
    expected_rbis = db.Column(db.Float, default=0.0)
    expected_stolen_bases = db.Column(db.Float, default=0.0)
    expected_caught_stealing = db.Column(db.Float, default=0.0)
    expected_ibb = db.Column(db.Float, default=0.0)
    expected_hbp = db.Column(db.Float, default=0.0)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<ExpectedGame {self.team_abbreviation} vs {self.handedness} {self.starter_expected_innings}IP>'
    
    def to_dict(self):
        """Convert expected game to dictionary."""
        return {
            'id': self.id,
            'team_abbreviation': self.team_abbreviation,
            'handedness': self.handedness,
            'starter_expected_innings': self.starter_expected_innings,
            'league_type': self.league_type,
            'scoring_settings': self.scoring_settings,
            'season': self.season,
            'expected_plate_appearances': self.expected_plate_appearances,
            'expected_fantasy_points': self.expected_fantasy_points,
            'expected_runs': self.expected_runs,
            'expected_hits': self.expected_hits,
            'expected_singles': self.expected_singles,
            'expected_doubles': self.expected_doubles,
            'expected_triples': self.expected_triples,
            'expected_home_runs': self.expected_home_runs,
            'expected_walks': self.expected_walks,
            'expected_strikeouts': self.expected_strikeouts,
            'expected_total_bases': self.expected_total_bases,
            'expected_rbis': self.expected_rbis,
            'expected_stolen_bases': self.expected_stolen_bases,
            'expected_caught_stealing': self.expected_caught_stealing,
            'expected_ibb': self.expected_ibb,
            'expected_hbp': self.expected_hbp,
            'created_at': self.created_at.isoformat() if self.created_at else None,
        }


class League(db.Model):
    """Model for storing league configurations and scoring settings."""
    
    __tablename__ = 'leagues'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    league_type = db.Column(db.String(20), nullable=False)  # 'Custom', 'ESPN', 'CBS', 'Yahoo'
    scoring_settings = db.Column(JSON)  # Custom scoring settings
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<League {self.name} ({self.league_type})>'
    
    def to_dict(self):
        """Convert league to dictionary."""
        return {
            'id': self.id,
            'name': self.name,
            'league_type': self.league_type,
            'scoring_settings': self.scoring_settings,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
        }
