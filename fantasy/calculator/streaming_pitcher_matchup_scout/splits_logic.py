from calculator.stat_finder.team_standing_getter import get_standings, return_wins_losses
from calculator.settings.team_object import Team
from calculator.stat_finder.team_hitting_getter import get_at_home_splits
from calculator.stat_finder.team_hitting_getter import get_away_splits
from calculator.stat_finder.team_hitting_getter import get_verse_lefty_splits
from calculator.stat_finder.team_hitting_getter import get_verse_righty_splits

TEAM_RECORD_MAP = {}
def get_team_record_map():
    standings_data = get_standings()
    for team in standings_data:
        # Get the standings and win/loss averages for all teams
        # print('getting standings for %s') % team['team_abbrev']
        win_avg, loss_avg, games, w_v_left, l_v_left, w_v_right, l_v_right, \
        w_at_home, l_at_home, w_on_road, l_on_road, g_v_left, g_v_right, \
        g_at_home, g_on_road = return_wins_losses(team)
        # Then create an object in the team map
        team_object = Team(t, win_avg, loss_avg, games, w_v_left, l_v_left,
            g_v_left, w_v_right, l_v_right,g_v_right, w_at_home, l_at_home, \
            g_at_home, w_on_road, l_on_road, g_on_road, team['team_id'])
        t = team['team_short'].replace(" ", "_").lower()
        TEAM_RECORD_MAP[t] = team_object

get_team_record_map()


# TEAM_AT_HOME_DICT = get_splits_by_uri(TEAM_AT_HOME_URI)
# TEAM_AWAY_DICT = get_splits_by_uri(TEAM_AWAY_URI)
# TEAM_VS_LEFTY_DICT = get_splits_by_uri(TEAM_VS_LEFTY_URI)
TEAM_VS_RIGHTY_DICT = get_verse_righty_splits()

print (TEAM_VS_RIGHTY_DICT)
