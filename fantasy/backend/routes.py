"""
API routes for the Fantasy Baseball application.
"""
from flask import Blueprint, request, jsonify
from marshmallow import Schema, fields, ValidationError
from services import FantasyCalculatorService, TeamService
from models import ScoringSettings, Team
import logging

logger = logging.getLogger(__name__)

# Create blueprint
api = Blueprint('api', __name__, url_prefix='/api')


# Validation schemas
class CalculateExpectedSchema(Schema):
    """Schema for validating expected points calculation requests."""
    handedness = fields.Str(required=True, validate=lambda x: x in ['Lefty', 'Righty'])
    inning = fields.Int(required=True, validate=lambda x: 1 <= x <= 9)
    league_type = fields.Str(required=True, validate=lambda x: x in ['Custom', 'ESPN', 'CBS', 'Yahoo'])
    custom_scoring = fields.Dict(missing=None)


class ScoringSettingsSchema(Schema):
    """Schema for validating scoring settings."""
    batting = fields.Dict(required=True)
    pitching = fields.Dict(required=True)


# Routes
@api.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    return jsonify({
        'status': 'healthy',
        'message': 'Fantasy Baseball API is running'
    })


@api.route('/scoring-settings/<league_type>', methods=['GET'])
def get_scoring_settings(league_type):
    """
    Get scoring settings for a specific league type.
    
    Args:
        league_type: League type (ESPN, CBS, Yahoo, Custom)
    """
    try:
        league_type = league_type.upper()
        
        if league_type not in ['ESPN', 'CBS', 'YAHOO', 'CUSTOM']:
            return jsonify({'error': 'Invalid league type'}), 400
        
        settings = FantasyCalculatorService.get_scoring_settings(league_type)
        
        return jsonify({
            'league_type': league_type,
            'scoring_settings': settings
        })
        
    except Exception as e:
        logger.error(f"Error getting scoring settings: {e}")
        return jsonify({'error': 'Internal server error'}), 500


@api.route('/teams', methods=['GET'])
def get_teams():
    """Get all teams with their statistics."""
    try:
        teams = TeamService.get_all_teams()
        return jsonify({
            'teams': teams,
            'count': len(teams)
        })
        
    except Exception as e:
        logger.error(f"Error getting teams: {e}")
        return jsonify({'error': 'Internal server error'}), 500


@api.route('/teams/<abbreviation>', methods=['GET'])
def get_team(abbreviation):
    """
    Get a specific team by abbreviation.
    
    Args:
        abbreviation: Team abbreviation (e.g., 'LAD')
    """
    try:
        team = TeamService.get_team_by_abbreviation(abbreviation.upper())
        
        if not team:
            return jsonify({'error': 'Team not found'}), 404
        
        return jsonify({'team': team})
        
    except Exception as e:
        logger.error(f"Error getting team {abbreviation}: {e}")
        return jsonify({'error': 'Internal server error'}), 500


@api.route('/calculate-expected', methods=['POST'])
def calculate_expected():
    """Calculate expected fantasy points for all teams."""
    try:
        # Validate request data
        schema = CalculateExpectedSchema()
        try:
            data = schema.load(request.json)
        except ValidationError as err:
            return jsonify({'error': 'Validation error', 'details': err.messages}), 400
        
        # Extract parameters
        handedness = data['handedness']
        inning = data['inning']
        league_type = data['league_type']
        custom_scoring = data.get('custom_scoring')
        
        # Validate custom scoring if provided
        if league_type == 'Custom' and custom_scoring:
            scoring_schema = ScoringSettingsSchema()
            try:
                scoring_schema.load(custom_scoring)
            except ValidationError as err:
                return jsonify({
                    'error': 'Invalid custom scoring settings',
                    'details': err.messages
                }), 400
        
        # Calculate expected points for all teams
        results = FantasyCalculatorService.calculate_all_teams_expected_points(
            handedness=handedness,
            inning=inning,
            league_type=league_type,
            custom_scoring=custom_scoring
        )
        
        return jsonify({
            'results': results,
            'parameters': {
                'handedness': handedness,
                'inning': inning,
                'league_type': league_type
            },
            'count': len(results)
        })
        
    except Exception as e:
        logger.error(f"Error calculating expected points: {e}")
        return jsonify({'error': 'Internal server error'}), 500


@api.route('/calculate-team-expected', methods=['POST'])
def calculate_team_expected():
    """Calculate expected fantasy points for a specific team."""
    try:
        data = request.json
        
        # Validate required fields
        required_fields = ['team_abbreviation', 'handedness', 'inning', 'league_type']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Missing required field: {field}'}), 400
        
        # Validate values
        if data['handedness'] not in ['Lefty', 'Righty']:
            return jsonify({'error': 'Invalid handedness'}), 400
        
        if not (1 <= data['inning'] <= 9):
            return jsonify({'error': 'Inning must be between 1 and 9'}), 400
        
        if data['league_type'] not in ['Custom', 'ESPN', 'CBS', 'Yahoo']:
            return jsonify({'error': 'Invalid league type'}), 400
        
        # Get scoring settings
        if data['league_type'] == 'Custom' and 'custom_scoring' in data:
            scoring_settings = data['custom_scoring']
        else:
            scoring_settings = FantasyCalculatorService.get_scoring_settings(data['league_type'])
        
        # Calculate expected points
        result = FantasyCalculatorService.calculate_expected_points(
            team_abbreviation=data['team_abbreviation'].upper(),
            handedness=data['handedness'],
            inning=data['inning'],
            scoring_settings=scoring_settings
        )
        
        return jsonify({'result': result})
        
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        logger.error(f"Error calculating team expected points: {e}")
        return jsonify({'error': 'Internal server error'}), 500


@api.route('/matchup-analysis', methods=['POST'])
def matchup_analysis():
    """
    Analyze matchups and return color-coded results.
    This endpoint provides additional analysis for the frontend visualization.
    """
    try:
        # Validate request data
        schema = CalculateExpectedSchema()
        try:
            data = schema.load(request.json)
        except ValidationError as err:
            return jsonify({'error': 'Validation error', 'details': err.messages}), 400
        
        # Calculate expected points for all teams
        results = FantasyCalculatorService.calculate_all_teams_expected_points(
            handedness=data['handedness'],
            inning=data['inning'],
            league_type=data['league_type'],
            custom_scoring=data.get('custom_scoring')
        )
        
        if not results:
            return jsonify({'error': 'No results found'}), 404
        
        # Calculate percentiles for color coding
        points = [r['expected_fantasy_points'] for r in results]
        min_points = min(points)
        max_points = max(points)
        
        # Add color coding based on percentiles
        for result in results:
            points_value = result['expected_fantasy_points']
            
            if max_points == min_points:
                # All teams have same expected points
                result['color_score'] = 0.5
                result['color_category'] = 'average'
            else:
                # Normalize to 0-1 scale
                normalized_score = (points_value - min_points) / (max_points - min_points)
                result['color_score'] = normalized_score
                
                # Categorize
                if normalized_score >= 0.7:
                    result['color_category'] = 'excellent'
                elif normalized_score >= 0.5:
                    result['color_category'] = 'good'
                elif normalized_score >= 0.3:
                    result['color_category'] = 'average'
                else:
                    result['color_category'] = 'poor'
        
        return jsonify({
            'results': results,
            'analysis': {
                'min_points': min_points,
                'max_points': max_points,
                'avg_points': sum(points) / len(points),
                'total_teams': len(results)
            },
            'parameters': {
                'handedness': data['handedness'],
                'inning': data['inning'],
                'league_type': data['league_type']
            }
        })
        
    except Exception as e:
        logger.error(f"Error in matchup analysis: {e}")
        return jsonify({'error': 'Internal server error'}), 500


@api.route('/team-stats', methods=['GET'])
def get_all_team_stats():
    """
    Get basic team stats for all teams (vs lefty and righty).
    This endpoint provides the raw data needed for frontend calculations.
    """
    try:
        teams = Team.query.all()
        
        if not teams:
            return jsonify({'error': 'No teams found'}), 404
        
        team_stats = []
        for team in teams:
            team_data = {
                'abbreviation': team.abbreviation,
                'name': team.name,
                'vs_lefty': {
                    'era': team.vs_lefty_era,
                    'whip': team.vs_lefty_whip,
                    'k_per_9': team.vs_lefty_k_per_9,
                    'bb_per_9': team.vs_lefty_bb_per_9,
                    'hr_per_9': team.vs_lefty_hr_per_9,
                    'hits_per_9': team.vs_lefty_hits_per_9,
                    'wins': team.vs_lefty_wins,
                    'losses': team.vs_lefty_losses
                },
                'vs_righty': {
                    'era': team.vs_righty_era,
                    'whip': team.vs_righty_whip,
                    'k_per_9': team.vs_righty_k_per_9,
                    'bb_per_9': team.vs_righty_bb_per_9,
                    'hr_per_9': team.vs_righty_hr_per_9,
                    'hits_per_9': team.vs_righty_hits_per_9,
                    'wins': team.vs_righty_wins,
                    'losses': team.vs_righty_losses
                }
            }
            team_stats.append(team_data)
        
        return jsonify({
            'teams': team_stats,
            'count': len(team_stats)
        })
        
    except Exception as e:
        logger.error(f"Error fetching team stats: {e}")
        return jsonify({'error': 'Internal server error'}), 500



# Error handlers
@api.errorhandler(404)
def not_found(error):
    """Handle 404 errors."""
    return jsonify({'error': 'Endpoint not found'}), 404


@api.errorhandler(405)
def method_not_allowed(error):
    """Handle 405 errors."""
    return jsonify({'error': 'Method not allowed'}), 405


@api.errorhandler(500)
def internal_error(error):
    """Handle 500 errors."""
    logger.error(f"Internal server error: {error}")
    return jsonify({'error': 'Internal server error'}), 500
