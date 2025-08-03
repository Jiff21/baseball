"""
Configuration settings for the Fantasy Baseball application.
"""
import os
from pathlib import Path

class Config:
    """Base configuration class."""
    
    # Database configuration
    BASE_DIR = Path(__file__).parent
    DATABASE_PATH = BASE_DIR / 'fantasy_baseball.db'
    SQLALCHEMY_DATABASE_URI = f'sqlite:///{DATABASE_PATH}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # API configuration
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    
    # CORS configuration
    CORS_ORIGINS = ['http://localhost:3000', 'http://127.0.0.1:3000']
    
    # MLB API configuration
    MLB_BASE_URL = 'https://www.mlb.com'
    
    # Team abbreviations
    MLB_TEAMS = [
        'COL', 'PIT', 'CWS', 'LAA', 'CLE', 'TEX', 'DET', 'MIN', 'BAL', 'KC',
        'SF', 'BOS', 'HOU', 'ATL', 'WSH', 'SD', 'MIL', 'CIN', 'OAK', 'MIA',
        'SEA', 'TB', 'NYM', 'STL', 'PHI', 'NYY', 'AZ', 'LAD', 'TOR', 'CHC'
    ]

class DevelopmentConfig(Config):
    """Development configuration."""
    DEBUG = True

class ProductionConfig(Config):
    """Production configuration."""
    DEBUG = False

class TestingConfig(Config):
    """Testing configuration."""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'

# Configuration mapping
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}

