"""
Unit tests for the Fantasy Baseball application.
"""
import pytest
import json
from app import create_app
from models import db, Team, ScoringSettings
from services import FantasyCalculatorService, TeamService


@pytest.fixture
def app():
    """Create and configure a test app."""
    app = create_app('testing')
    
    with app.app_context():
        db.create_all()
        
        # Add sample team data
        sample_team = Team(
            abbreviation='LAD',
            name='Los Angeles Dodgers',
            vs_lefty_era=3.50,
            vs_lefty_whip=1.20,
            vs_lefty_k_per_9=9.0,
            vs_lefty_bb_per_9=3.0,
            vs_lefty_hr_per_9=1.0,
            vs_lefty_hits_per_9=8.0,
            vs_righty_era=3.60,
            vs_righty_whip=1.25,
            vs_righty_k_per_9=8.5,
            vs_righty_bb_per_9=3.2,
            vs_righty_hr_per_9=1.1,
            vs_righty_hits_per_9=8.2
        )
        db.session.add(sample_team)
        db.session.commit()
        
        yield app
        
        db.drop_all()


@pytest.fixture
def client(app):
    """Create a test client."""
    return app.test_client()


class TestScoringSettings:
    """Test scoring settings functionality."""
    
    def test_get_default_settings(self):
        """Test getting default scoring settings."""
        settings = ScoringSettings.get_default_settings()
        
        assert 'batting' in settings
        assert 'pitching' in settings
        assert settings['batting']['HR'] == 4
        assert settings['pitching']['W'] == 5.0
    
    def test_get_espn_settings(self):
        """Test getting ESPN scoring settings."""
        settings = ScoringSettings.get_espn_settings()
        
        assert settings['batting']['HR'] == 4
        assert settings['pitching']['W'] == 7
    
    def test_get_cbs_settings(self):
        """Test getting CBS scoring settings."""
        settings = ScoringSettings.get_cbs_settings()
        
        assert settings['batting']['SO'] == -0.5
        assert settings['pitching']['QS'] == 3.0
    
    def test_get_yahoo_settings(self):
        """Test getting Yahoo scoring settings."""
        settings = ScoringSettings.get_yahoo_settings()
        
        assert settings['batting']['HR'] == 10.4
        assert settings['pitching']['SO'] == 3.0


class TestFantasyCalculatorService:
    """Test fantasy calculator service."""
    
    def test_get_scoring_settings(self):
        """Test getting scoring settings by league type."""
        espn_settings = FantasyCalculatorService.get_scoring_settings('ESPN')
        assert espn_settings['batting']['HR'] == 4
        
        cbs_settings = FantasyCalculatorService.get_scoring_settings('CBS')
        assert cbs_settings['batting']['SO'] == -0.5
        
        yahoo_settings = FantasyCalculatorService.get_scoring_settings('Yahoo')
        assert yahoo_settings['batting']['HR'] == 10.4
        
        custom_settings = FantasyCalculatorService.get_scoring_settings('Custom')
        assert custom_settings['batting']['HR'] == 4
    
    def test_calculate_expected_points(self, app):
        """Test calculating expected points for a team."""
        with app.app_context():
            scoring_settings = ScoringSettings.get_default_settings()
            
            result = FantasyCalculatorService.calculate_expected_points(
                team_abbreviation='LAD',
                handedness='Righty',
                inning=6,
                scoring_settings=scoring_settings
            )
            
            assert result['team_abbreviation'] == 'LAD'
            assert result['handedness'] == 'Righty'
            assert result['inning'] == 6
            assert 'expected_fantasy_points' in result
            assert 'expected_hits' in result
            assert 'team_stats' in result
    
    def test_calculate_expected_points_invalid_team(self, app):
        """Test calculating expected points for invalid team."""
        with app.app_context():
            scoring_settings = ScoringSettings.get_default_settings()
            
            with pytest.raises(ValueError, match="Team INVALID not found"):
                FantasyCalculatorService.calculate_expected_points(
                    team_abbreviation='INVALID',
                    handedness='Righty',
                    inning=6,
                    scoring_settings=scoring_settings
                )


class TestTeamService:
    """Test team service."""
    
    def test_get_all_teams(self, app):
        """Test getting all teams."""
        with app.app_context():
            teams = TeamService.get_all_teams()
            
            assert len(teams) == 1
            assert teams[0]['abbreviation'] == 'LAD'
            assert teams[0]['name'] == 'Los Angeles Dodgers'
    
    def test_get_team_by_abbreviation(self, app):
        """Test getting team by abbreviation."""
        with app.app_context():
            team = TeamService.get_team_by_abbreviation('LAD')
            
            assert team is not None
            assert team['abbreviation'] == 'LAD'
            assert team['name'] == 'Los Angeles Dodgers'
    
    def test_get_team_by_abbreviation_not_found(self, app):
        """Test getting team by abbreviation when not found."""
        with app.app_context():
            team = TeamService.get_team_by_abbreviation('INVALID')
            
            assert team is None


class TestAPIRoutes:
    """Test API routes."""
    
    def test_health_check(self, client):
        """Test health check endpoint."""
        response = client.get('/api/health')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['status'] == 'healthy'
    
    def test_get_scoring_settings(self, client):
        """Test getting scoring settings endpoint."""
        response = client.get('/api/scoring-settings/ESPN')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['league_type'] == 'ESPN'
        assert 'scoring_settings' in data
    
    def test_get_scoring_settings_invalid(self, client):
        """Test getting scoring settings with invalid league type."""
        response = client.get('/api/scoring-settings/INVALID')
        
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'error' in data
    
    def test_get_teams(self, client):
        """Test getting teams endpoint."""
        response = client.get('/api/teams')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'teams' in data
        assert 'count' in data
        assert data['count'] == 1
    
    def test_get_team(self, client):
        """Test getting specific team endpoint."""
        response = client.get('/api/teams/LAD')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'team' in data
        assert data['team']['abbreviation'] == 'LAD'
    
    def test_get_team_not_found(self, client):
        """Test getting team that doesn't exist."""
        response = client.get('/api/teams/INVALID')
        
        assert response.status_code == 404
        data = json.loads(response.data)
        assert 'error' in data
    
    def test_calculate_expected(self, client):
        """Test calculate expected endpoint."""
        request_data = {
            'handedness': 'Righty',
            'inning': 6,
            'league_type': 'ESPN'
        }
        
        response = client.post('/api/calculate-expected', 
                             data=json.dumps(request_data),
                             content_type='application/json')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'results' in data
        assert 'parameters' in data
        assert len(data['results']) == 1
    
    def test_calculate_expected_invalid_data(self, client):
        """Test calculate expected with invalid data."""
        request_data = {
            'handedness': 'Invalid',
            'inning': 10,
            'league_type': 'ESPN'
        }
        
        response = client.post('/api/calculate-expected',
                             data=json.dumps(request_data),
                             content_type='application/json')
        
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'error' in data
    
    def test_calculate_team_expected(self, client):
        """Test calculate team expected endpoint."""
        request_data = {
            'team_abbreviation': 'LAD',
            'handedness': 'Righty',
            'inning': 6,
            'league_type': 'ESPN'
        }
        
        response = client.post('/api/calculate-team-expected',
                             data=json.dumps(request_data),
                             content_type='application/json')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'result' in data
        assert data['result']['team_abbreviation'] == 'LAD'


if __name__ == '__main__':
    pytest.main([__file__])

