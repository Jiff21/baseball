import os
from datetime import datetime

year = datetime.now().strftime('%Y')
today = datetime.now().strftime('%Y/%m/%d')

# YEAR_FOR_HITTING_STATS = os.getenv('YEAR_FOR_HITTING_STATS', year)
YEAR_FOR_HITTING_STATS = os.getenv('YEAR_FOR_HITTING_STATS', '2017')
DATE_FOR_STANDINGS = os.getenv('DATE_FOR_STANDINGS', today)

BASE_URL = 'http://mlb.mlb.com/lookup/json/'
TEAM_STATS_URI     = 'named.team_hitting_season_leader_master.bam?season=' + YEAR_FOR_HITTING_STATS + '&sort_order=%27desc%27&sort_column=%27avg%27&game_type=%27R%27&sport_code=%27mlb%27&recSP=1&recPP=50'
SPLITS_URI = 'named.team_hitting_season_leader_sit.bam?season=' \
    + YEAR_FOR_HITTING_STATS \
    + '&sort_order=%27desc%27&sort_column=%27avg%27&game_type=%27R%27&sport_code=%27mlb%27'
TEAM_AT_HOME_URI   = SPLITS_URI + '&sit_code=%27h%27&recSP=1&recPP=50'
TEAM_AWAY_URI      = SPLITS_URI + '&sit_code=%27a%27&recSP=1&recPP=50'
TEAM_VS_LEFTY_URI  = SPLITS_URI + '&sit_code=%27vl%27&recSP=1&recPP=50'
TEAM_VS_RIGHTY_URI = SPLITS_URI + '&sit_code=%27vr%27&recSP=1&recPP=50'

TEAM_STANDING_URI = \
    'named.standings_schedule_date.bam?season=2017&schedule_game_date.game_date=%27' \
    + DATE_FOR_STANDINGS \
    + '%27&sit_code=%27h0%27&league_id=103&league_id=104&all_star_sw=%27N%27&version=2'
