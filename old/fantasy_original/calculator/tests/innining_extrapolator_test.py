from full_season_forecaster.pitcher_inning_extrapelator import inning_extrapolator

season_innings = 72.1
season_starts = 11.0
season_era = 2.89
season_win_total = 5.0
season_loss_total = 3.0
season_hits_allowed = 78.0  
season_home_runs = 11.0
season_walk_total = 23.0
season_strikeouts = 66.0
projected_starts = 31.0
projected_fip =  4.37


new_season_total = inning_extrapolator(season_innings, season_starts, season_era, season_win_total, \
	season_loss_total, season_hits_allowed, season_home_runs, season_walk_total, season_strikeouts, \
	projected_starts, projected_fip)
