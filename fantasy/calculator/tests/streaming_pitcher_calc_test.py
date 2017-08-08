from tests.stubbed_data.standings import Standings
from settings.team_record_map import return_wins_losses, get_record_map, create_teams


TEAM_STANDING_DICT = Standings.TEAM_STANDING_DICT


TEAM_RECORD_MAP = get_record_map(Standings.ALL_TEAM_SHORT_NAMES, Standings.TEAM_STANDING_DICT)

houston_win_losses = get_record_map(Standings(Houston))

assert houston_win_losses.win_avg == 0.724137

# loss_avg, games, w_v_left, l_v_left, w_v_right, l_v_right, w_at_home, \
                # l_at_home, w_on_road, l_on_road, g_v_left, g_v_right, g_at_home, g_on_road