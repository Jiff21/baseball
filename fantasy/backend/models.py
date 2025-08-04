"""
Database models for the Fantasy Baseball application.
"""
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import JSON

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
        GIDP = 0   # Grounded into double play
        E = 0      # Errors

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
        TB = 0       # Total Bases
        Hold = 0     # Holds
        WP = 0       # Wild Pitch
        BK = 0       # Balk

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
                'GIDP': cls.Batting.GIDP,
                'E': cls.Batting.E,
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
                'Hold': cls.Pitching.Hold,
                'WP': cls.Pitching.WP,
                'BK': cls.Pitching.BK,
            }
        }

    @classmethod
    def get_espn_settings(cls):
        """Get ESPN scoring settings."""
        return {
            'batting': {
                'S': 1, 'D': 2, 'T': 3, 'HR': 4, 'BB': 1, 'IBB': 0,
                'HBP': 1, 'R': 1, 'RBI': 1, 'SB': 2, 'CS': -1, 'SO': -0.5,
                'GIDP': 0, 'E': 0,
            },
            'pitching': {
                'BB': -1, 'IBB': 0, 'ER': -1, 'HA': -1, 'HB': 0, 'HRA': 0,
                'INN': 3, 'K': 0.5, 'W': 7, 'L': -5, 'S': 5, 'BS': 0,
                'QS': 3, 'TB': 0, 'Hold': 0, 'WP': 0, 'BK': 0,
            }
        }

    @classmethod
    def get_cbs_settings(cls):
        """Get CBS scoring settings."""
        return {
            'batting': {
                'S': 1.0, 'D': 2.0, 'T': 3.0, 'HR': 4.0, 'BB': 1.0, 'IBB': 0.0,
                'HBP': 1.0, 'R': 1.0, 'RBI': 1.0, 'SB': 2.0, 'CS': -1.0, 'SO': -0.5,
                'GIDP': 0.0, 'E': 0.0,
            },
            'pitching': {
                'BB': -1.0, 'IBB': 0.0, 'ER': -1.0, 'HA': -1.0, 'HB': -1.0, 'HRA': 0.0,
                'INN': 3.0, 'K': 0.5, 'W': 7.0, 'L': -5.0, 'S': 7.0, 'BS': 0.0,
                'QS': 3.0, 'TB': 0.0, 'Hold': 0.0, 'WP': 0.0, 'BK': 0.0,
            }
        }
    

    @classmethod
    def get_yahoo_settings(cls):
        """Get Yahoo scoring settings."""
        return {
            'batting': {
                'S': 2.6, 'D': 5.2, 'T': 7.8, 'HR': 10.4, 'BB': 2.6, 'IBB': 0.0,
                'HBP': 2.6, 'R': 1.9, 'RBI': 1.9, 'SB': 4.2, 'CS': 0.0, 'SO': 0.0,
                'GIDP': 0.0, 'E': 0.0,
            },
            'pitching': {
                'BB': -1.3, 'IBB': 0.0, 'ER': -3.0, 'HA': -1.3, 'HB': -1.3, 'HRA': 0.0,
                'INN': 3.0, 'K': 3.0, 'W': 7.0, 'L': 0.0, 'S': 8.0, 'BS': 0.0,
                'QS': 0.0, 'TB': 0.0, 'Hold': 0.0, 'WP': 0.0, 'BK': 0.0,
            }
        }

class Team(db.Model):
    """Model for MLB teams and their stats."""
    
    __tablename__ = 'teams'
    
    id = db.Column(db.Integer, primary_key=True)
    abbreviation = db.Column(db.String(3), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    
    # Pitching stats vs lefty batters
    vs_lefty_era = db.Column(db.Float, default=0.0)
    vs_lefty_whip = db.Column(db.Float, default=0.0)
    vs_lefty_k_per_9 = db.Column(db.Float, default=0.0)
    vs_lefty_bb_per_9 = db.Column(db.Float, default=0.0)
    vs_lefty_hr_per_9 = db.Column(db.Float, default=0.0)
    vs_lefty_hits_per_9 = db.Column(db.Float, default=0.0)
    vs_lefty_wins = db.Column(db.Integer, default=0)
    vs_lefty_losses = db.Column(db.Integer, default=0)
    
    # Pitching stats vs righty batters
    vs_righty_era = db.Column(db.Float, default=0.0)
    vs_righty_whip = db.Column(db.Float, default=0.0)
    vs_righty_k_per_9 = db.Column(db.Float, default=0.0)
    vs_righty_bb_per_9 = db.Column(db.Float, default=0.0)
    vs_righty_hr_per_9 = db.Column(db.Float, default=0.0)
    vs_righty_hits_per_9 = db.Column(db.Float, default=0.0)
    vs_righty_wins = db.Column(db.Integer, default=0)
    vs_righty_losses = db.Column(db.Integer, default=0)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<Team {self.abbreviation}: {self.name}>'
    
    def to_dict(self):
        """Convert team to dictionary."""
        return {
            'id': self.id,
            'abbreviation': self.abbreviation,
            'name': self.name,
            'vs_lefty': {
                'era': self.vs_lefty_era,
                'whip': self.vs_lefty_whip,
                'k_per_9': self.vs_lefty_k_per_9,
                'bb_per_9': self.vs_lefty_bb_per_9,
                'hr_per_9': self.vs_lefty_hr_per_9,
                'hits_per_9': self.vs_lefty_hits_per_9,
                'wins': self.vs_lefty_wins,
                'losses': self.vs_lefty_losses,
            },
            'vs_righty': {
                'era': self.vs_righty_era,
                'whip': self.vs_righty_whip,
                'k_per_9': self.vs_righty_k_per_9,
                'bb_per_9': self.vs_righty_bb_per_9,
                'hr_per_9': self.vs_righty_hr_per_9,
                'hits_per_9': self.vs_righty_hits_per_9,
                'wins': self.vs_righty_wins,
                'losses': self.vs_righty_losses,
            },
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
        }


class ExpectedGame(db.Model):
    """Model for storing expected game calculations."""
    
    __tablename__ = 'expected_games'
    
    id = db.Column(db.Integer, primary_key=True)
    team_abbreviation = db.Column(db.String(3), db.ForeignKey('teams.abbreviation'), nullable=False)
    handedness = db.Column(db.String(10), nullable=False)  # 'Lefty' or 'Righty'
    inning = db.Column(db.Integer, default=6)
    league_type = db.Column(db.String(20), nullable=False)  # 'Custom', 'ESPN', 'CBS', 'Yahoo'
    scoring_settings = db.Column(JSON)  # JSON field for scoring settings
    
    # Expected stats
    expected_fantasy_points = db.Column(db.Float, default=0.0)
    expected_runs = db.Column(db.Float, default=0.0)
    expected_hits = db.Column(db.Float, default=0.0)
    expected_home_runs = db.Column(db.Float, default=0.0)
    expected_strikeouts = db.Column(db.Float, default=0.0)
    expected_walks = db.Column(db.Float, default=0.0)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationship
    team = db.relationship('Team', backref=db.backref('expected_games', lazy=True))
    
    def __repr__(self):
        return f'<ExpectedGame {self.team_abbreviation} vs {self.handedness}>'
    
    def to_dict(self):
        """Convert expected game to dictionary."""
        return {
            'id': self.id,
            'team_abbreviation': self.team_abbreviation,
            'handedness': self.handedness,
            'inning': self.inning,
            'league_type': self.league_type,
            'scoring_settings': self.scoring_settings,
            'expected_fantasy_points': self.expected_fantasy_points,
            'expected_runs': self.expected_runs,
            'expected_hits': self.expected_hits,
            'expected_home_runs': self.expected_home_runs,
            'expected_strikeouts': self.expected_strikeouts,
            'expected_walks': self.expected_walks,
            'created_at': self.created_at.isoformat() if self.created_at else None,
        }
