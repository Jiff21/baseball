import os
from datetime import datetime

year = datetime.now().strftime('%Y')
today = datetime.now().strftime('%Y/%m/%d')
year = '2019'
# today = '2019/10/30'

YEAR_FOR_HITTING_STATS = os.getenv('YEAR_FOR_HITTING_STATS', year)
DATE_FOR_STANDINGS = os.getenv('DATE_FOR_STANDINGS', today)

BASE_URL = 'http://mlb.mlb.com/lookup/json/'
UPDATED_BASE_URL = 'http://lookup-service-prod.mlb.com/json/'

TEAM_HITTING_JSON_BLOCK = 'team_hitting_season_leader_master'

TEAM_STATS_URI = TEAM_HITTING_JSON_BLOCK + '?season=' \
    + YEAR_FOR_HITTING_STATS \
    + '&sort_order=%27desc%27&sort_column=%27avg%27&game_type=%27R%27&sport_code=%27mlb%27'

# SPLITS_URI = 'named.team_hitting_season_leader_sit.bam?season=' \
SPLITS_URI =  TEAM_HITTING_JSON_BLOCK + '?season=' \
    + YEAR_FOR_HITTING_STATS \
    + '&sort_order=%27desc%27&sort_column=%27avg%27&game_type=%27R%27&sport_code=%27mlb%27'
END_QUAL = '&recSP=1&recPP=50'
# Home Away splits different?
# http://lookup-service-prod.mlb.com/json/named.team_hitting_season_leader_sit.bam?season=2019&sort_order=%27desc%27&sort_column=%27avg%27&game_type=%27R%27&sport_code=%27mlb%27&sit_code=%27vr%27&recSP=1&recPP=50
TEAM_AT_HOME_URI   = SPLITS_URI + '&sit_code=%27h%27' + END_QUAL
TEAM_AWAY_URI      = SPLITS_URI + '&sit_code=%27a%27' + END_QUAL
TEAM_VS_LEFTY_URI  = SPLITS_URI + '&sit_code=%27vl%27' + END_QUAL
TEAM_VS_RIGHTY_URI = SPLITS_URI + '&sit_code=%27vr%27' + END_QUAL

TEAM_STANDING_URI = \
    'named.standings_schedule_date.bam?season=' \
    + YEAR_FOR_HITTING_STATS \
    + '&schedule_game_date.game_date=%27' \
    + DATE_FOR_STANDINGS \
    + '%27&sit_code=%27h0%27&league_id=103&league_id=104&all_star_sw=%27N%27&version=2'
# Updated URL for Above but would need to reformat for json resplonse
STATS_API = 'https://statsapi.mlb.com/api/v1/'
STANDINGS_URI = 'standings?leagueId=103,104&season=2019&standingsTypes=regularSeason,springTraining,firstHalf,secondHalf&hydrate=division,conference,sport,league,team(nextSchedule(team,gameType=[R,F,D,L,W,C],inclusive=false),previousSchedule(team,gameType=[R,F,D,L,W,C],inclusive=true))'
