# Fantasy Baseball Expected Start

A comprehensive fantasy baseball application that calculates expected fantasy points for MLB team matchups based on batter handedness, innings, and league scoring settings.

## Features

### Frontend (React + TypeScript)
- **Fantasy Expected Start Component**: Main interface for calculating expected points
- **Handedness Selection**: Choose between Lefty and Righty batters
- **League Type Selection**: Support for Custom, ESPN, CBS, and Yahoo scoring
- **Inning Input**: Specify innings (1-9) with validation
- **Custom Scoring Settings**: Full customization of batting and pitching scoring
- **Local Storage**: Save and load custom league configurations
- **Color-Coded Visualization**: Teams displayed with gradient colors based on matchup quality
- **Detailed Team Analysis**: Click teams for comprehensive stat breakdowns
- **Responsive Design**: Works on desktop and mobile devices

### Backend (Python + Flask)
- **RESTful API**: JSON API for all data operations
- **SQLite Database**: Stores team stats and expected game calculations
- **MLB Data Scraper**: Collects and updates team statistics
- **Fantasy Calculator Service**: Calculates expected points using various scoring systems
- **Multiple League Support**: ESPN, CBS, Yahoo, and custom scoring settings
- **Team Statistics**: Pitching stats vs lefty and righty batters
- **Comprehensive Testing**: Unit tests for all major components

## Project Structure

```
fantasy/
├── backend/                 # Python Flask API
│   ├── app.py              # Main Flask application
│   ├── config.py           # Configuration settings
│   ├── models.py           # Database models
│   ├── routes.py           # API endpoints
│   ├── services.py         # Business logic services
│   ├── scraper.py          # MLB data scraper
│   ├── requirements.txt    # Python dependencies
│   └── test_app.py         # Backend tests
├── frontend/               # React TypeScript app
│   ├── public/             # Static files
│   ├── src/
│   │   ├── components/     # React components
│   │   │   ├── FantasyExpectedStart.tsx
│   │   │   ├── ScoringSettingsForm.tsx
│   │   │   ├── TeamMatchupGrid.tsx
│   │   │   ├── FantasyExpectedStart.css
│   │   │   └── __tests__/  # Component tests
│   │   ├── services/       # API services
│   │   ├── types/          # TypeScript definitions
│   │   ├── utils/          # Utility functions
│   │   └── App.tsx         # Main App component
│   ├── package.json        # Node dependencies
│   └── tsconfig.json       # TypeScript config
└── tests/                  # End-to-end tests
```

## Getting Started

### Prerequisites
- Python 3.8+
- Node.js 16+
- npm or yarn

### Backend Setup

1. Navigate to the backend directory:
```bash
cd fantasy/backend
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Initialize the database:
```bash
python app.py
```

5. Run the development server:
```bash
python app.py
```

The API will be available at `http://localhost:8000`

### Frontend Setup

1. Navigate to the frontend directory:
```bash
cd fantasy/frontend
```

2. Install dependencies:
```bash
npm install
```

3. Start the development server:
```bash
npm start
```

The React app will be available at `http://localhost:3000`

## API Endpoints

### Health Check
- `GET /api/health` - API health check

### Scoring Settings
- `GET /api/scoring-settings/{league_type}` - Get scoring settings for a league type

### Teams
- `GET /api/teams` - Get all teams with statistics
- `GET /api/teams/{abbreviation}` - Get specific team by abbreviation

### Calculations
- `POST /api/calculate-expected` - Calculate expected points for all teams
- `POST /api/calculate-team-expected` - Calculate expected points for specific team
- `POST /api/matchup-analysis` - Get color-coded matchup analysis

## Scoring Systems

### Default/Custom Scoring
- Fully customizable batting and pitching scoring
- Save custom leagues to localStorage
- Default values based on standard fantasy baseball scoring

### ESPN Scoring
- Standard ESPN public league scoring
- Preset values that cannot be modified

### CBS Scoring
- CBS Sports fantasy baseball scoring
- Includes quality starts and adjusted strikeout values

### Yahoo Scoring
- Yahoo Sports fantasy baseball scoring
- Higher point values for offensive categories

## Team Statistics

The application tracks the following pitching statistics for each MLB team, split by batter handedness:

- **ERA**: Earned Run Average
- **WHIP**: Walks + Hits per Inning Pitched
- **K/9**: Strikeouts per 9 innings
- **BB/9**: Walks per 9 innings
- **HR/9**: Home runs allowed per 9 innings
- **H/9**: Hits allowed per 9 innings

## Testing

### Backend Tests
```bash
cd fantasy/backend
pytest test_app.py -v
```

### Frontend Tests
```bash
cd fantasy/frontend
npm test
```

### Run All Tests
```bash
# Backend
cd fantasy/backend && pytest test_app.py

# Frontend
cd fantasy/frontend && npm test -- --coverage --watchAll=false
```

## Development

### Adding New Teams
Teams are automatically populated by the scraper. To add new teams manually:

1. Add team data to the `team_names` dictionary in `scraper.py`
2. Run the scraper: `python scraper.py`

### Customizing Scoring
To add new scoring systems:

1. Add new method to `ScoringSettings` class in `models.py`
2. Update `get_scoring_settings` method in `services.py`
3. Add new option to frontend dropdown

### Database Schema
The application uses SQLite with the following main tables:

- **teams**: MLB team information and pitching statistics
- **expected_games**: Calculated expected game results

## Deployment

### Backend Deployment
1. Set environment variables:
   - `FLASK_ENV=production`
   - `SECRET_KEY=your-secret-key`

2. Use a production WSGI server like Gunicorn:
```bash
gunicorn -w 4 -b 0.0.0.0:8000 app:app
```

### Frontend Deployment
1. Build the production bundle:
```bash
npm run build
```

2. Serve the `build` directory with a web server

### Environment Variables
- `REACT_APP_API_URL`: Backend API URL (default: http://localhost:8000/api)
- `FLASK_ENV`: Flask environment (development/production)
- `SECRET_KEY`: Flask secret key for production

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Ensure all tests pass
6. Submit a pull request

## License

This project is licensed under the MIT License.

## Support

For questions or issues, please open a GitHub issue or contact the development team.

