"""
New Flask application for Fantasy Baseball - Hitting Stats Focus.
This replaces the old pitching-focused app with a hitting-based approach.
"""
from flask import Flask, request, jsonify
from flask_cors import CORS
import logging
import os
from datetime import datetime

# Import new models and services
from models_new import db, TeamHittingStats, TeamCalculatedStats, ExpectedGame, League, ScoringSettings
from services.hitting_stats_service import HittingStatsService
from services.calculation_service import CalculationService
from config import Config

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def create_app(config_name='development'):
    """Create and configure the Flask application."""
    app = Flask(__name__)
    
    # Load configuration
    if config_name == 'development':
        app.config.from_object(Config)
    
    # Initialize extensions
    db.init_app(app)
    CORS(app)
    
    # Create database tables
    with app.app_context():
        db.create_all()
        logger.info("Database tables created successfully")
    
    # Initialize services
    hitting_service = HittingStatsService()
    calc_service = CalculationService()
    
    @app.route('/api/health', methods=['GET'])
    def health_check():
        """Health check endpoint."""
        return jsonify({
            'status': 'healthy',
            'timestamp': datetime.utcnow().isoformat(),
            'version': '2.0.0-refactor'
        })
    
    @app.route('/api/fetch-hitting-stats', methods=['POST'])
    def fetch_hitting_stats():
        """Fetch and store hitting statistics from MLB APIs."""
        try:
            season = request.json.get('season', datetime.now().year)
            
            logger.info(f"Fetching hitting stats for {season} season...")
            
            # Fetch all hitting stats
            hitting_service_instance = HittingStatsService(season=season)
            all_stats = hitting_service_instance.fetch_all_hitting_stats()
            
            # Store raw hitting stats and calculate rates
            stored_teams = []
            calculated_teams = []
            
            for split_type, teams_data in all_stats.items():
                for team_abbrev, team_data in teams_data.items():
                    # Store raw hitting stats
                    hitting_stats = TeamHittingStats.query.filter_by(
                        team_abbreviation=team_abbrev,
                        split_type=split_type,
                        season=season
                    ).first()
                    
                    if hitting_stats:
                        # Update existing record
                        for key, value in team_data.items():
                            if hasattr(hitting_stats, key):
                                setattr(hitting_stats, key, value)
                    else:
                        # Create new record
                        hitting_stats = TeamHittingStats(**team_data)
                        db.session.add(hitting_stats)
                    
                    stored_teams.append(f"{team_abbrev}-{split_type}")
                    
                    # Calculate per-PA rates
                    rates = calc_service.calculate_per_pa_rates(team_data)
                    
                    # Store calculated rates
                    calculated_stats = TeamCalculatedStats.query.filter_by(
                        team_abbreviation=team_abbrev,
                        split_type=split_type,
                        season=season
                    ).first()
                    
                    if calculated_stats:
                        # Update existing record
                        for key, value in rates.items():
                            if hasattr(calculated_stats, key):
                                setattr(calculated_stats, key, value)
                    else:
                        # Create new record
                        calculated_stats = TeamCalculatedStats(**rates)
                        db.session.add(calculated_stats)
                    
                    calculated_teams.append(f"{team_abbrev}-{split_type}")
            
            # Commit all changes
            db.session.commit()
            
            logger.info(f"Successfully stored hitting stats for {len(stored_teams)} team-split combinations")
            
            return jsonify({
                'success': True,
                'message': f'Successfully fetched and stored hitting stats for {season}',
                'stored_teams': len(stored_teams),
                'calculated_teams': len(calculated_teams),
                'season': season
            })
            
        except Exception as e:
            db.session.rollback()
            logger.error(f"Error fetching hitting stats: {e}")
            return jsonify({
                'success': False,
                'error': str(e)
            }), 500
    
    @app.route('/api/teams/<team_abbrev>/stats', methods=['GET'])
    def get_team_stats(team_abbrev):
        """Get hitting statistics for a specific team."""
        try:
            season = request.args.get('season', datetime.now().year, type=int)
            
            # Get raw hitting stats for all splits
            hitting_stats = TeamHittingStats.query.filter_by(
                team_abbreviation=team_abbrev.upper(),
                season=season
            ).all()
            
            # Get calculated rates for all splits
            calculated_stats = TeamCalculatedStats.query.filter_by(
                team_abbreviation=team_abbrev.upper(),
                season=season
            ).all()
            
            if not hitting_stats:
                return jsonify({
                    'success': False,
                    'error': f'No stats found for team {team_abbrev} in {season}'
                }), 404
            
            # Organize data by split type
            team_data = {
                'team_abbreviation': team_abbrev.upper(),
                'season': season,
                'splits': {}
            }
            
            for stats in hitting_stats:
                split_type = stats.split_type
                team_data['splits'][split_type] = {
                    'raw_stats': stats.to_dict(),
                    'calculated_rates': None
                }
            
            for stats in calculated_stats:
                split_type = stats.split_type
                if split_type in team_data['splits']:
                    team_data['splits'][split_type]['calculated_rates'] = stats.to_dict()
            
            return jsonify({
                'success': True,
                'data': team_data
            })
            
        except Exception as e:
            logger.error(f"Error getting team stats: {e}")
            return jsonify({
                'success': False,
                'error': str(e)
            }), 500
    
    @app.route('/api/calculate-expected', methods=['POST'])
    def calculate_expected():
        """Calculate expected statistics for a team vs specific handedness."""
        try:
            data = request.json
            team_abbrev = data.get('team_abbreviation', '').upper()
            handedness = data.get('handedness', 'righty').lower()  # 'lefty' or 'righty'
            starter_innings = data.get('starter_expected_innings', 6.0)
            league_type = data.get('league_type', 'Custom')
            custom_scoring = data.get('scoring_settings')
            season = data.get('season', datetime.now().year)
            
            # Get calculated rates for the team and handedness
            calculated_stats = TeamCalculatedStats.query.filter_by(
                team_abbreviation=team_abbrev,
                split_type=handedness,
                season=season
            ).first()
            
            if not calculated_stats:
                return jsonify({
                    'success': False,
                    'error': f'No calculated stats found for {team_abbrev} vs {handedness} in {season}'
                }), 404
            
            # Get scoring settings
            if custom_scoring:
                scoring_settings = custom_scoring
            elif league_type == 'ESPN':
                scoring_settings = ScoringSettings.get_espn_settings()
            elif league_type == 'CBS':
                scoring_settings = ScoringSettings.get_cbs_settings()
            elif league_type == 'Yahoo':
                scoring_settings = ScoringSettings.get_yahoo_settings()
            else:
                scoring_settings = ScoringSettings.get_default_settings()
            
            # Calculate expected statistics
            rates_dict = calculated_stats.to_dict()
            expected_stats = calc_service.calculate_expected_stats(
                rates_dict, starter_innings, scoring_settings
            )
            
            # Store the expected game calculation
            expected_game = ExpectedGame(
                team_abbreviation=team_abbrev,
                handedness=handedness,
                starter_expected_innings=starter_innings,
                league_type=league_type,
                scoring_settings=scoring_settings,
                season=season,
                **{k: v for k, v in expected_stats.items() if k.startswith('expected_')}
            )
            
            db.session.add(expected_game)
            db.session.commit()
            
            return jsonify({
                'success': True,
                'data': expected_stats,
                'calculation_id': expected_game.id
            })
            
        except Exception as e:
            db.session.rollback()
            logger.error(f"Error calculating expected stats: {e}")
            return jsonify({
                'success': False,
                'error': str(e)
            }), 500
    
    @app.route('/api/debug/raw-stats-csv', methods=['GET'])
    def export_raw_stats_csv():
        """Export raw hitting statistics to CSV for debugging."""
        try:
            season = request.args.get('season', datetime.now().year, type=int)
            
            # Get all raw hitting stats
            hitting_stats = TeamHittingStats.query.filter_by(season=season).all()
            
            if not hitting_stats:
                return jsonify({
                    'success': False,
                    'error': f'No raw stats found for {season}'
                }), 404
            
            # Convert to CSV format
            import csv
            import io
            
            output = io.StringIO()
            writer = csv.writer(output)
            
            # Write header
            header = [
                'team_abbreviation', 'team_name', 'split_type', 'season',
                'games', 'plate_appearances', 'at_bats', 'runs', 'hits',
                'singles', 'doubles', 'triples', 'home_runs', 'rbis',
                'walks', 'intentional_walks', 'hit_by_pitch', 'strikeouts',
                'stolen_bases', 'caught_stealing', 'total_bases', 'wins', 'losses'
            ]
            writer.writerow(header)
            
            # Write data
            for stats in hitting_stats:
                row = [
                    stats.team_abbreviation, stats.team_name, stats.split_type, stats.season,
                    stats.games, stats.plate_appearances, stats.at_bats, stats.runs, stats.hits,
                    stats.singles, stats.doubles, stats.triples, stats.home_runs, stats.rbis,
                    stats.walks, stats.intentional_walks, stats.hit_by_pitch, stats.strikeouts,
                    stats.stolen_bases, stats.caught_stealing, stats.total_bases, stats.wins, stats.losses
                ]
                writer.writerow(row)
            
            csv_content = output.getvalue()
            output.close()
            
            return csv_content, 200, {
                'Content-Type': 'text/csv',
                'Content-Disposition': f'attachment; filename=raw_hitting_stats_{season}.csv'
            }
            
        except Exception as e:
            logger.error(f"Error exporting raw stats CSV: {e}")
            return jsonify({
                'success': False,
                'error': str(e)
            }), 500
    
    @app.route('/api/debug/calculated-stats-csv', methods=['GET'])
    def export_calculated_stats_csv():
        """Export calculated per-PA rates to CSV for debugging."""
        try:
            season = request.args.get('season', datetime.now().year, type=int)
            
            # Get all calculated stats
            calculated_stats = TeamCalculatedStats.query.filter_by(season=season).all()
            
            if not calculated_stats:
                return jsonify({
                    'success': False,
                    'error': f'No calculated stats found for {season}'
                }), 404
            
            # Convert to CSV format
            import csv
            import io
            
            output = io.StringIO()
            writer = csv.writer(output)
            
            # Write header
            header = [
                'team_abbreviation', 'split_type', 'season',
                'strikeouts_per_pa', 'runs_per_pa', 'walks_per_pa',
                'singles_per_pa', 'doubles_per_pa', 'triples_per_pa', 'home_runs_per_pa',
                'total_bases_per_pa', 'ibb_per_pa', 'hbp_per_pa', 'rbis_per_pa',
                'stolen_bases_per_pa', 'caught_stealing_per_pa', 'pa_per_inning',
                'wins_per_game', 'losses_per_game'
            ]
            writer.writerow(header)
            
            # Write data
            for stats in calculated_stats:
                row = [
                    stats.team_abbreviation, stats.split_type, stats.season,
                    stats.strikeouts_per_pa, stats.runs_per_pa, stats.walks_per_pa,
                    stats.singles_per_pa, stats.doubles_per_pa, stats.triples_per_pa, stats.home_runs_per_pa,
                    stats.total_bases_per_pa, stats.ibb_per_pa, stats.hbp_per_pa, stats.rbis_per_pa,
                    stats.stolen_bases_per_pa, stats.caught_stealing_per_pa, stats.pa_per_inning,
                    stats.wins_per_game, stats.losses_per_game
                ]
                writer.writerow(row)
            
            csv_content = output.getvalue()
            output.close()
            
            return csv_content, 200, {
                'Content-Type': 'text/csv',
                'Content-Disposition': f'attachment; filename=calculated_stats_{season}.csv'
            }
            
        except Exception as e:
            logger.error(f"Error exporting calculated stats CSV: {e}")
            return jsonify({
                'success': False,
                'error': str(e)
            }), 500
    
    @app.route('/api/scoring-settings', methods=['GET'])
    def get_scoring_settings():
        """Get available scoring settings."""
        return jsonify({
            'success': True,
            'data': {
                'default': ScoringSettings.get_default_settings(),
                'espn': ScoringSettings.get_espn_settings(),
                'cbs': ScoringSettings.get_cbs_settings(),
                'yahoo': ScoringSettings.get_yahoo_settings()
            }
        })
    
    logger.info(f"Flask app created with config: {config_name}")
    return app


if __name__ == '__main__':
    app = create_app()
    port = int(os.environ.get('PORT', 8000))
    logger.info(f"Starting Flask app on port {port} (debug=False)")
    app.run(host='0.0.0.0', port=port, debug=False)
