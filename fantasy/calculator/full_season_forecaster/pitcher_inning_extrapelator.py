from calculator.settings.scoring_settings import ScoringSettings
ssp = ScoringSettings.Pitching

def inning_extrapolator(season_innings, season_starts, season_era, season_win_total, \
	season_loss_total, season_hits_allowed, season_home_runs, season_walk_total, season_strikeouts, \
	projected_starts, projected_fip):

	innings_projection = round(projected_starts * (season_innings / season_starts), 1)
	points_from_innings = round(innings_projection * ssp.INN, 1)
	# print 'Innings Projection is: ' + str(innings_projection)
	# print 'points_from_innings Projection is:\n ' + str(points_from_innings)
	# print '\n\n'

	projected_win_percentage = season_win_total / season_starts
	points_from_wins = round((projected_starts * projected_win_percentage) * ssp.W, 0)

	projected_loss_percentage = season_loss_total / season_starts
	points_from_losses = round((projected_starts * projected_loss_percentage) * ssp.L, 0)
	# print 'projected_win_percentage Projection is:\n ' + str(projected_win_percentage)
	# print 'points_from_wins Projection is:\n ' + str(points_from_wins)
	# print '\n\n'
	# print 'projected_loss_percentage Projection is:\n ' + str(projected_loss_percentage)
	# print 'points_from_losses Projection is:\n ' + str(points_from_losses)
	# print '\n\n'

	points_from_earned_runs = round((innings_projection * (season_era/9)), 2) * ssp.ER
	# print 'points_from_earned_runs Projection is:\n ' + str(points_from_earned_runs)
	# print '\n\n'

	homerun_rate = season_home_runs/season_innings
	projected_hra = round(homerun_rate * innings_projection, 0)
	points_from_home_runs = int(projected_hra * ssp.HRA)
	# print 'homerun_rate Projection is:\n ' + str(homerun_rate)
	# print 'projected_hra Projection is:\n ' + str(projected_hra)
	# print 'points_from_home_runs Projection is:\n ' + str(points_from_home_runs)
	# print '\n\n'

	strikeout_rate = season_strikeouts/season_innings
	projected_stikeouts = round(strikeout_rate * innings_projection, 0)
	points_from_strikeouts = int(projected_stikeouts * ssp.K)
	# print 'strikeout_rate Projection is:\n ' + str(strikeout_rate)
	# print 'projected_stikeouts Projection is:\n ' + str(projected_stikeouts)
	# print 'points_from_strikeouts Projection is:\n ' + str(points_from_strikeouts)
	# print '\n\n'


	hit_rate = season_hits_allowed/season_innings
	projected_hits = round(hit_rate * innings_projection, 0)
	points_from_hits = int(projected_hits * ssp.HA)
	# print 'hit_rate Projection is:\n ' + str(hit_rate)
	# print 'projected_hits Projection is:\n ' + str(projected_hits)
	# print 'points_from_hits Projection is:\n ' + str(points_from_hits)
	# print '\n\n'


	walk_rate = season_walk_total/season_innings
	projected_walks = round(walk_rate * innings_projection, 0)
	points_from_walks = int(projected_walks * ssp.BB)
	# print 'walk_rate Projection is:\n ' + str(walk_rate)
	# print 'projected_walks Projection is:\n ' + str(projected_walks)
	# print 'points_from_walks Projection is:\n ' + str(points_from_walks)
	# print '\n\n'



	next_season_total = points_from_innings + points_from_strikeouts + points_from_wins \
		+ points_from_losses + points_from_hits + points_from_walks + points_from_home_runs \
		+ points_from_earned_runs
	print ('Next Seasons Total based on ERA would be: ' + str(next_season_total))

	points_from_fip_runs = round((innings_projection * (projected_fip/9)), 2) * ssp.ER
	next_season_total = points_from_innings + points_from_strikeouts + points_from_wins \
		+ points_from_losses + points_from_hits + points_from_walks + points_from_home_runs \
		+ points_from_fip_runs
	print( 'Next Seasons Total based on ERA would be: ' + str(next_season_total) )
