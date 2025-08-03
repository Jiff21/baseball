import time
from behave import given, when, then, step
from calculator.settings.team_object import Team

@given('We create MIN as a default team')
def step_impl(context):
    mlb = {}
    ta = 'MIN'
    team = Team()
    team.abbr = ta
    mlb[team.abbr] = team
    mlb[ta].away_bb_pg = 2.935483870967742
    mlb[ta].away_h_pg = 10.03225806451613
    mlb[ta].away_hr_pg = 2.1451612903225805
    mlb[ta].away_r_pg = 6.209677419354839
    mlb[ta].away_so_pg = 8.306451612903226
    mlb[ta].expected_game_away_split = 11.9
    mlb[ta].expected_game_home_split = 13.5
    mlb[ta].expected_game_lefty_split = 9.6
    mlb[ta].expected_game_no_split = 12.6
    mlb[ta].expected_game_righty_split = 13.6
    mlb[ta].g_at_home = 68.0
    mlb[ta].g_at_road = 62.0
    mlb[ta].g_v_left = 30.0
    mlb[ta].g_v_right = 100.0
    mlb[ta].games = 130
    mlb[ta].hits_per_game = 9.592307692307692
    mlb[ta].home_bb_pg = 3.3676470588235294
    mlb[ta].home_h_pg = 9.191176470588236
    mlb[ta].home_hr_pg = 1.7647058823529411
    mlb[ta].home_r_pg = 5.529411764705882
    mlb[ta].home_so_pg = 8.029411764705882
    mlb[ta].homeruns_per_game = 1.9461538461538461
    mlb[ta].id = 142
    mlb[ta].l_avg_home = 0.4264705882352941
    mlb[ta].l_avg_road = 0.3548387096774194
    mlb[ta].loss_avg = 0.3923076923076923
    mlb[ta].loss_avg_right = 0.37
    mlb[ta].losses = 51
    mlb[ta].losses_avg_left = 0.4666666666666667
    mlb[ta].plate_appearences_per_game = 39.48461538461538
    mlb[ta].run_avg = 5.8538461538461535
    mlb[ta].runs_per_game = 5.8538461538461535
    mlb[ta].standings=None
    mlb[ta].strikeouts_per_game = 8.161538461538461
    mlb[ta].total_plate_appearances = 5133
    mlb[ta].vs_l_bb_per_pa = 0.08169219547775347
    mlb[ta].vs_l_h_per_pa = 0.25966447848285923
    mlb[ta].vs_l_hr_per_pa = 0.05616338439095551
    mlb[ta].vs_l_r_per_pa = 0.1611962071480671
    mlb[ta].vs_l_so_per_pa = 0.19839533187454414
    mlb[ta].vs_r_bb_per_pa = 0.07947900053163211
    mlb[ta].vs_r_h_per_pa = 0.23684210526315788
    mlb[ta].vs_r_hr_per_pa = 0.04678362573099415
    mlb[ta].vs_r_r_per_pa = 0.14354066985645933
    mlb[ta].vs_r_so_per_pa = 0.20972886762360446
    mlb[ta].w_avg_home = 0.63
    mlb[ta].w_avg_road = 0.6451612903225806
    mlb[ta].walks_per_game = 3.1615384615384614
    mlb[ta].win_avg = 0.6076923076923076
    mlb[ta].wins = 79
    mlb[ta].wins_avg_left = 0.5333333333333333
    mlb[ta].wins_avg_right = 0.63
