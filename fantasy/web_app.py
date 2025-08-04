from flask import Flask, render_template, request, redirect, url_for
from calculator.settings.scoring_settings import ScoringSettings

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/league-setup')
def league_setup():
    # Get current scoring settings
    batting_settings = {
        'Singles': ScoringSettings.Batting.S,
        'Doubles': ScoringSettings.Batting.D,
        'Triples': ScoringSettings.Batting.T,
        'Home Runs': ScoringSettings.Batting.HR,
        'Walks': ScoringSettings.Batting.BB,
        'Intentional Walks': ScoringSettings.Batting.IBB,
        'Hit By Pitch': ScoringSettings.Batting.HBP,
        'Runs': ScoringSettings.Batting.R,
        'Runs Batted In': ScoringSettings.Batting.RBI,
        'Stolen Base': ScoringSettings.Batting.SB,
        'Caught Stealing': ScoringSettings.Batting.CS,
        'Strike Outs': ScoringSettings.Batting.SO
    }
    
    pitching_settings = {
        'Walks Issued': ScoringSettings.Pitching.BB,
        'IBB': ScoringSettings.Pitching.BBI,
        'Earned Runs': ScoringSettings.Pitching.ER,
        'Hits allowed': ScoringSettings.Pitching.HA,
        'Hit Batters': ScoringSettings.Pitching.HB,
        'HRA': ScoringSettings.Pitching.HRA,
        'Innings': ScoringSettings.Pitching.INN,
        'Strikeouts': ScoringSettings.Pitching.K,
        'Wins': ScoringSettings.Pitching.W,
        'Losses': ScoringSettings.Pitching.L,
        'Saves': ScoringSettings.Pitching.S,
        'Blown Saves': getattr(ScoringSettings.Pitching, 'BS', 0),
        'Quality Starts': ScoringSettings.Pitching.QS,
        'Total Bases': 0  # This doesn't exist in current settings, defaulting to 0
    }
    
    return render_template('league_setup.html', 
                         batting_settings=batting_settings,
                         pitching_settings=pitching_settings)

@app.route('/update-scoring', methods=['POST'])
def update_scoring():
    # Handle form submission to update scoring settings
    # This would update the scoring settings based on form data
    return redirect(url_for('league_setup'))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
