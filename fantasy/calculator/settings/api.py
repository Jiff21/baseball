import os
from datetime import datetime
from calculator.settings.logger import log

year = datetime.now().strftime('%Y')
today = datetime.now().strftime('%Y-%m-%d')
year = '2022'
# today = '2019/10/30'

YEAR_FOR_HITTING_STATS = os.getenv('YEAR_FOR_HITTING_STATS', year)
DATE_FOR_STANDINGS = os.getenv('DATE_FOR_STANDINGS', today)

BASE_URL = 'http://mlb.mlb.com/lookup/json/'
UPDATED_BASE_URL = 'https://bdfed.stitch.mlbinfra.com/bdfed/stats/team'

TEAM_HITTING_JSON_BLOCK = '?stitch_env=prod&sportId=1&gameType=R&group=hitting&order=desc&sortStat=onBasePlusSlugging&stats=season'

TEAM_STATS_URI = TEAM_HITTING_JSON_BLOCK + '&season=' \
    + YEAR_FOR_HITTING_STATS \
    + '&limit=30&offset=0'

# SPLITS_URI = 'named.team_hitting_season_leader_sit.bam?season=' \
SPLITS_URI =  TEAM_HITTING_JSON_BLOCK + '?season=' \
    + YEAR_FOR_HITTING_STATS \
    + '&sort_order=%27desc%27&sort_column=%27avg%27&game_type=%27R%27&sport_code=%27mlb%27'
# This may no longer be necessary but doesn't seem to stop data.
END_QUAL = '&recSP=1&recPP=50'

TEAM_AT_HOME_URI   = SPLITS_URI + '&sitCodes=h' + END_QUAL
TEAM_AWAY_URI      = SPLITS_URI + '&sitCodes=a' + END_QUAL
TEAM_VS_LEFTY_URI  = SPLITS_URI + '&sitCodes=vl' + END_QUAL
TEAM_VS_RIGHTY_URI = SPLITS_URI + '&sitCodes=v4' + END_QUAL

TEAM_STANDING_URL = \
    'https://statsapi.mlb.com/api/v1/standings?leagueId=103,104&season=' \
    + YEAR_FOR_HITTING_STATS \
    + '&date=' \
    + DATE_FOR_STANDINGS \
    + '&standingsTypes=regularSeason,springTraining,firstHalf,secondHalf&hydrate=division,conference,sport,league,team(nextSchedule(team,gameType=[R,F,D,L,W,C],inclusive=false),previousSchedule(team,gameType=[R,F,D,L,W,C],inclusive=true))'


# Updated URL for Above but would need to reformat for json resplonse
STATS_API = 'https://statsapi.mlb.com/api/v1/'
STANDINGS_URI = 'standings?leagueId=103,104&season=2019&standingsTypes=regularSeason,springTraining,firstHalf,secondHalf&hydrate=division,conference,sport,league,team(nextSchedule(team,gameType=[R,F,D,L,W,C],inclusive=false),previousSchedule(team,gameType=[R,F,D,L,W,C],inclusive=true))'
