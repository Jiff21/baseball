from calculator.settings.logger import log
from calculator.settings.scoring_settings import ScoringSettings


ssp = ScoringSettings.Pitching


def inning_extrapolator(season_innings, season_starts, season_era, season_win_total, \
	season_loss_total, season_hits_allowed, season_home_runs, season_walk_total, season_strikeouts, \
	projected_starts, projected_fip):
	innings_projection = round(projected_starts * (season_innings / season_starts), 1)
	points_from_innings = round(innings_projection * ssp.INN, 1)
	log.debug( 'Innings Projection is: ' + str(innings_projection))
	log.debug( 'points_from_innings Projection is:\n ' + str(points_from_innings))
	log.debug( '\n\n')


	projected_win_percentage = season_win_total / season_starts
	points_from_wins = round((projected_starts * projected_win_percentage) * ssp.W, 0)


	projected_loss_percentage = season_loss_total / season_starts
	points_from_losses = round((projected_starts * projected_loss_percentage) * ssp.L, 0)
	log.debug( 'projected_win_percentage Projection is:\n ' + str(projected_win_percentage))
	log.debug( 'points_from_wins Projection is:\n ' + str(points_from_wins))
	log.debug( '\n\n')
	log.debug( 'projected_loss_percentage Projection is:\n ' + str(projected_loss_percentage))
	log.debug( 'points_from_losses Projection is:\n ' + str(points_from_losses))
	log.debug( '\n\n')


	points_from_earned_runs = round((innings_projection * (season_era/9)), 2) * ssp.ER
	log.debug( 'points_from_earned_runs Projection is:\n ' + str(points_from_earned_runs))
	log.debug( '\n\n')


	homerun_rate = season_home_runs/season_innings
	projected_hra = round(homerun_rate * innings_projection, 0)
	points_from_home_runs = int(projected_hra * ssp.HRA)
	log.debug( 'homerun_rate Projection is:\n ' + str(homerun_rate))
	log.debug( 'projected_hra Projection is:\n ' + str(projected_hra))
	log.debug( 'points_from_home_runs Projection is:\n ' + str(points_from_home_runs))
	log.debug( '\n\n')

	strikeout_rate = season_strikeouts/season_innings
	projected_stikeouts = round(strikeout_rate * innings_projection, 0)
	points_from_strikeouts = int(projected_stikeouts * ssp.K)
	log.debug( 'strikeout_rate Projection is:\n ' + str(strikeout_rate))
	log.debug( 'projected_stikeouts Projection is:\n ' + str(projected_stikeouts))
	log.debug( 'points_from_strikeouts Projection is:\n ' + str(points_from_strikeouts))
	log.debug( '\n\n')


	hit_rate = season_hits_allowed/season_innings
	projected_hits = round(hit_rate * innings_projection, 0)
	points_from_hits = int(projected_hits * ssp.HA)
	log.debug( 'hit_rate Projection is:\n ' + str(hit_rate))
	log.debug( 'projected_hits Projection is:\n ' + str(projected_hits))
	log.debug( 'points_from_hits Projection is:\n ' + str(points_from_hits))
	log.debug( '\n\n')


	walk_rate = season_walk_total/season_innings
	projected_walks = round(walk_rate * innings_projection, 0)
	points_from_walks = int(projected_walks * ssp.BB)
	log.debug( 'walk_rate Projection is:\n ' + str(walk_rate))
	log.debug( 'projected_walks Projection is:\n ' + str(projected_walks))
	log.debug( 'points_from_walks Projection is:\n ' + str(points_from_walks))
	log.debug( '\n\n')


	next_season_total = points_from_innings + points_from_strikeouts + points_from_wins \
		+ points_from_losses + points_from_hits + points_from_walks + points_from_home_runs \
		+ points_from_earned_runs
	log.debug('Next Seasons Total based on ERA would be: ' + str(next_season_total))


	points_from_fip_runs = round((innings_projection * (projected_fip/9)), 2) * ssp.ER
	next_season_total = points_from_innings + points_from_strikeouts + points_from_wins \
		+ points_from_losses + points_from_hits + points_from_walks + points_from_home_runs \
		+ points_from_fip_runs
	log.debug( 'Next Seasons Total based on ERA would be: ' + str(next_season_total) )

	return next_season_total
