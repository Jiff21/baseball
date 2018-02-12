from full_season_forecaster.pitcher_inning_extrapelator import inning_extrapolator

def input_last_season_stats():
	season_innings = float(raw_input('How many Innings Pitched Last Season?\n                                  '))
	season_starts = float(raw_input('How many Game Starts Last Season?\n                                    '))
	season_era = float(raw_input('What was the ERA Last Season?\n                           '))
	season_home_runs = float(raw_input('How Many Home Runs Last Season?\n                           '))
	season_strikeouts = float(raw_input('How Many Strikeouts Last Season?\n                               '))
	season_win_total = float(raw_input('How Many Wins Last Season?\n                        '))
	season_loss_total = float(raw_input('How many Losses Last Season?\n                           '))
	season_hits_allowed = float(raw_input('How Many Hits Last Season?\n                          '))
	season_walk_total = float(raw_input('How Many Walks last season?\n                             '))
	projected_starts = float(raw_input('How many starts next season?\n                           '))
	projected_fip = float(raw_input('What was the FIP\n                           '))
	return season_innings, season_starts, season_era, season_win_total, season_loss_total, \
		season_hits_allowed, season_home_runs, season_walk_total, season_strikeouts, projected_starts, projected_fip


season_innings, season_starts, season_era, season_win_total, season_loss_total, season_hits_allowed, \
	season_home_runs, season_walk_total, season_strikeouts, projected_starts, projected_fip = input_last_season_stats()

new_season_total = inning_extrapolator(season_innings, season_starts, season_era, season_win_total, \
	season_loss_total, season_hits_allowed, season_home_runs, season_walk_total, season_strikeouts, \
	projected_starts, projected_fip)
