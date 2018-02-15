class Team(object):
    def __init__(self, name=None, win_avg=None, loss_avg=None, games=None, \
        w_v_left=None, l_v_left=None, g_v_left=None, \
        w_v_right=None, l_v_right=None,g_v_right=None, \
        w_at_home=None, l_at_home=None, g_at_home=None, \
        w_on_road=None, l_on_road=None, g_on_road=None, team_id=None):
        """Return a team and there win loss splits."""
        self.name = name
        self.win_avg = win_avg
        self.games = games
        self.loss_avg = loss_avg
        self.w_v_left = w_v_left
        self.l_v_left = l_v_left
        self.w_v_right = w_v_right
        self.l_v_right = l_v_right
        self.w_at_home = w_at_home
        self.l_at_home = l_at_home
        self.w_on_road = w_on_road
        self.l_on_road = l_on_road
        self.g_v_left = g_v_left
        self.g_v_right = g_v_left
        self.g_at_home = g_v_left
        self.g_on_road = g_v_left
        self.team_id = team_id
